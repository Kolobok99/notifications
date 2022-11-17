import datetime
from datetime import time

import arrow
import requests
from django.conf import settings
from django.db.models import Q, QuerySet
from django.utils import timezone

from apps.mailings import models as mailing_models


def get_or_create_region_code_by_phone(phone: mailing_models.Client.phone) -> mailing_models.RegionCode:
    """
        Получает code (код мобильного оператора) из phone
        Получает инстанс RegionCode по code или создает если такого не существует

        Args:
            phone (Client.phone): атрибут phone инстанса модели Client из прил. mailings

        Returns:
              полученный/созданный инстанс RegionCode из прил. mailings
    """

    code = phone[1:4]
    region_code = mailing_models.RegionCode.objects.get_or_create(code=code)[0]

    return region_code


def clients_generator_by_mailing_filters(mailing: mailing_models.Mailing) -> QuerySet[mailing_models.Client]:
    """
        Делает выборку из модели Client у которых
        region_code in [mailing.filter_codes.all()]
        или
        tags in  [mailing.filter_tags.all()]

        Args:
              mailing (Mailing): инстанс модели Mailing из прил. mailings

        Returns:
              множество инстансов модели Client для переданной mailing
    """

    if not mailing.filter_codes.count() and not mailing.filter_tags.count():
        return mailing_models.Client.objects.all()
    else:
        return mailing_models.Client.objects.filter(
            Q(region_code__in=mailing.filter_codes.all()) |
            Q(tags__in=mailing.filter_tags.all())
        )


def messages_generator_by_clients_in_mailing(mailing: mailing_models.Mailing, clients: QuerySet[mailing_models.Client]) -> [mailing_models.Message]:
    """
        Перебирает множество clients и генерирует для каждого
        message:
                .mailing = переданный mailing
                .client = текущий client итерации

        Args:
              mailing (Mailing): инстанс модели Mailing из прил. mailings
              clients (Client): множество инстансов модели Client для mailing
        Returns:
              множество messages для каждого client в рамках mailing
    """

    return [mailing_models.Message.objects.create(mailing=mailing, client=client) for client in clients]


def messages_sender(messages: QuerySet[mailing_models.Message]) -> None:
    """ Обновляет статус писем и генерирует отправку сообщений со статусом CREATED

      Перебирает переданный список messages и для каждого message:
      обновляет их статус: message = updating_message_status_by_time(message)
      генерирует отправку post-запроса для message со status=CREATED: send_message_by_fbrq_api(message)

      Args:
          messages (mailing_models.Message):
            множество инстансов модели Message одной рассылки из прил. mailing
    """

    #"""Генерирует отправку переданных messages на FBRQ API"""

    for index, message in enumerate(messages):
        message = updating_message_status_by_time(message)
        if message.status == 'CREATED':
            send_message_by_fbrq_api(message)
        elif message.status == 'IS_OVER':
            messages[index:].update(status='IS_OVER')
            break


def send_message_by_fbrq_api(msg: mailing_models.Message) -> requests.status_codes:
    """
        Отправляет msg на номер msg.client.phone,
        генерируя post-запрос на https://probe.fbrq.cloud/v1/send/{msg.pk}

        Args:
              msg (Message): инстанс модели Message из прил. mailings
        Return:
              http код ответа на post-запрос

    """

    url = f"https://probe.fbrq.cloud/v1/send/{msg.pk}"
    token = settings.API_KEY

    headers = {
        'Authorization': token,
    }
    payload = {
        "id": msg.pk,
        "phone": str(msg.client.phone),
        "text": msg.mailing.text
    }

    r = requests.post(url=url, headers=headers, json=payload)

    if r.status_code == 200:
        msg.status = '200'
    else:
        msg.status = '400'
    msg.save()

    return r.status_code


def updating_message_status_by_time(message: mailing_models.Message) -> mailing_models.Message:
    """
    Обновляет статус переданного сообщения на
        IS_OVER: если текущее время больше message.mailing.end_time
        LIMITED: если текущее время клиента не входит во временной интервал message.mailing

    Args:
        message (Message): инстанс модели Message из прил. mailings

    Returns:
            переданное message с обновленным статусом

    """

    current_time = timezone.now()
    client_time_local = converter_utc_time_to_client_local_time(message.client)

    if current_time >= message.mailing.end_time:
        message.status = 'IS_OVER'
    elif not (message.mailing.time_interval_start < client_time_local < message.mailing.time_interval_end):
        message.status = "LIMITED"
    message.save()

    return message


def converter_utc_time_to_client_local_time(client: mailing_models.Client) -> time:
    """
        Конвертирует локальное время  client  во время в формате utc + 0

        Args:
            client (Client): инстанс модели Client из прил. mailings

        Return:
              локальное время client в формате utc+0
    """

    current_date_utc = arrow.utcnow()

    current_client_time = current_date_utc + datetime.timedelta(hours=client.timezone)

    return current_client_time.time()


def mailing_statistic_generator(mailing: mailing_models.Mailing) -> None:
    """
        Генерирует статистику для mailing (static.mailing = mailing)

        Args:
            mailing (Mailing): инстанс модели Mailing прил. mailings
    """

    msgs = mailing_models.Message.objects.filter(mailing=mailing)
    statistic = mailing_models.MailingStatistic(mailing=mailing)

    statistic.msg_count = msgs.count()
    statistic.created_count = msgs.filter(status='CREATED').count()
    statistic.sent_count = msgs.filter(status='SENT').count()
    statistic.delivered_count = msgs.filter(status='200').count()
    statistic.errors_count = msgs.filter(status='400').count()
    statistic.is_overed_count = msgs.filter(status='IS_OVER').count()
    statistic.is_limited_count = msgs.filter(status='LIMITED').count()

    statistic.report += "-----------------------------------\n"
    statistic.report += f"Рассылка номер: {mailing.pk}\n"
    statistic.report += f"Всего сообщений: {statistic.created_count}\n"
    statistic.report += f"Успешно доставлено: {statistic.delivered_count}\n"
    statistic.report += f"Не доставлено: {statistic.errors_count}\n"
    statistic.report += f"Не доставлено по времени: {statistic.is_overed_count}\n"
    statistic.report += f"Не доставлено по времененному интервалу: {statistic.is_limited_count}\n"

    statistic.save()
