from django.conf import settings
from django.utils import timezone

from conf.celery import app

from apps.mailings import models as mailing_models
from services.mailings_services import clients_generator_by_mailing_filters, \
    messages_generator_by_clients_in_mailing, messages_sender, \
    mailing_statistic_generator, send_email


@app.task
def task_mailing(mailing_pk: mailing_models.Mailing.pk) -> None:
    """
        TASK: рассылка сообщений в рамках mailing.pk = mailing_pk:
        1) Генериурет список клиентов
        2) Генерирует сообщений для созданных клиентов
        3) Отправляет сообщения клиентам
        4) Создает отчет законченной рассылки

        Args:
            mailing_pk (int): ID инстанса модели mailing прил. mailings
    """

    mailing = mailing_models.Mailing.objects.get(pk=mailing_pk)
    mailing.status = 'S'
    mailing.save()

    clients = clients_generator_by_mailing_filters(mailing)

    messages = messages_generator_by_clients_in_mailing(mailing, clients)

    messages_sender(messages)

    mailing_statistic_generator(mailing=mailing)
    mailing.status = 'F'
    mailing.save()


@app.task
def task_send_statistics_to_admin(admin_email=settings.ADMIN_EMAIL) -> None:
    """
        Делает выборку mailings: (Mailing), запущенных today,
        Собирает отчеты: statistic.report всех mailings,
        Отправялет письмо с собранными отчетами на admin_email

        Args:
            admin_email (str): Email админа из settings.ADMIN_EMAIL, если не передан другой

    """

    today = timezone.now()
    try:
        mailings = mailing_models.Mailing.objects.filter(start_time__day=today.day)
        statistics = ""
        for mailing in mailings:
            statistics += mailing.statistic.report
        send_email(email=admin_email,
                   message_header=f'Статистика за {today.day}.{today.month}',
                   message=statistics)
    except:
        pass
