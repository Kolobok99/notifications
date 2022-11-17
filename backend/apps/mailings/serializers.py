from typing import OrderedDict

from rest_framework import serializers, validators

from apps.mailings import models as mailing_models
from apps.mailings import validators as mailing_custom_validators
from conf.celery import app
from conf.settings import logger

from services import mailings_services, polls_services


class ClientSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Client"""

    def create(self, validated_data):
        phone = validated_data.get('phone')
        validated_data['region_code'] = mailings_services.get_or_create_region_code_by_phone(phone)

        instance = super(ClientSerializer, self).create(validated_data)
        logger.debug(f'CREATE <CLIENT_phone_{instance.phone}>(t_z={instance.timezone}; '
                     f'code={instance.region_code}; '
                     f'tags={[t.tag for t in instance.tags.all()]})')

        logger.debug(f'UPDATE <CLIENT_phone_{instance.phone}> -> ({validated_data.get("phone", instance.phone)})'
                     f'(t_z={instance.timezone} -> ({validated_data.get("timezone", instance.timezone)}); '
                     f'code={instance.region_code} -> ({validated_data.get("region_code", instance.region_code)}); '
                     f'tags={[t.tag for t in instance.tags.all()]} -> ({validated_data.get("tags", [t.tag for t in instance.tags.all()])}))')

        return instance

    def update(self, instance, validated_data):
        new_phone = validated_data.get('phone')
        if new_phone != instance.phone:
            validated_data['region_code'] = mailings_services.get_or_create_region_code_by_phone(new_phone)

        instance = super(ClientSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = mailing_models.Client

        fields = "__all__"
        extra_kwargs = {
            'phone': {'validators': [
                mailing_custom_validators.PhoneNumberValidator,
                validators.UniqueValidator(
                    queryset=mailing_models.Client.objects.all(),
                    message='ошибка: клиент с таким номером уже существует'
                )
            ]},
            'region_code': {'read_only': True}
        }


class ClientTagSerializer(serializers.ModelSerializer):
    """Сериалайзер модели ClientTag"""

    class Meta:
        model = mailing_models.ClientTag
        fields = "__all__"
        extra_kwargs = {
            'tag': {'validators': [
                mailing_custom_validators.ClientTagValidator,
                validators.UniqueValidator(
                    queryset=mailing_models.ClientTag.objects.all(),
                    message='ошибка: такой тег уже существует'
                )
            ]},
        }


class MailingStatisticSerializer(serializers.ModelSerializer):
    """Сериалайзер модели MailingStatistic"""

    class Meta:
        model = mailing_models.MailingStatistic
        fields = ['mailing', 'msg_count', 'created_count',
                   'sent_count', 'delivered_count', 'errors_count',
                   'is_overed_count', 'is_limited_count'
                ]

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)


class MailingSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Mailing"""

    statistic = MailingStatisticSerializer(read_only=True, many=False)

    def create(self, validated_data):
        instance = super(MailingSerializer, self).create(validated_data)
        polls_services.mailing_task_creator_and_task_id_updator(instance)
        logger.debug(f'CREATE <MAILING_pk_{instance.pk}> '
                     f'start_time={instance.start_time}; end_time={instance.end_time};'
                     f'text={instance.text};'
                     f'filter_codes={[t.code for t in instance.filter_codes.all()]};'
                     f'filter_tags={[t.tag for t in instance.filter_tags.all()]})')
        return instance

    def update(self, instance: mailing_models.Mailing, validated_data: OrderedDict) -> mailing_models.Mailing:
        app.control.revoke(task_id=instance.task_id, terminate=True, signal="SIGKILL")
        instance = super().update(instance, validated_data)
        instance = polls_services.mailing_task_creator_and_task_id_updator(instance)
        logger.debug(f'UPDATE <MAILING_pk_{instance.pk}> '
                     f'start_time={instance.start_time} -> ({validated_data.get("start_time", instance.start_time)});'
                     f' end_time={instance.end_time}; -> ({validated_data.get("end_time", instance.end_time)})'
                     f'text={instance.text};  -> ({validated_data.get("text", instance.text)})'
                     f'filter_codes={[t.code for t in instance.filter_codes.all()]}; ->'
                     f'({validated_data.get("filter_codes", [t.code for t in instance.filter_codes.all()])})'
                     f'filter_tags={[t.tag for t in instance.filter_tags.all()]}) ->'
                     f'({validated_data.get("filter_tags", [t.tag for t in instance.filter_tags.all()])})'
                     )

        return instance

    class Meta:
        model = mailing_models.Mailing
        fields = ('id', 'status', 'start_time', 'end_time',
                  'text', 'filter_codes', 'filter_tags',
                  'task_id', 'time_interval_start', 'time_interval_end', 'statistic',)
        validators = [
            mailing_custom_validators.MailingStartTimeValidator,
            mailing_custom_validators.MailingEndTimeValidator,
            mailing_custom_validators.MailingTimeIntervalValidator,
        ]
        extra_kwargs = {
            'status': {'source': 'get_status_display'},
        }