from typing import OrderedDict

from rest_framework import serializers, validators

from apps.mailings import models as mailing_models
from apps.mailings import validators as mailing_custom_validators
from conf.celery import app

from services import mailings_services, polls_services


class ClientSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Client"""

    def create(self, validated_data):
        phone = validated_data.get('phone')
        validated_data['region_code'] = mailings_services.get_or_create_region_code_by_phone(phone)

        instance = super(ClientSerializer, self).create(validated_data)

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
        fields = "__all__"


class MailingSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Mailing"""

    statistic = MailingStatisticSerializer(read_only=True, many=False)

    def create(self, validated_data):
        instance = super(MailingSerializer, self).create(validated_data)
        polls_services.mailing_task_creator_and_task_id_updator(instance)

        return instance

    def update(self, instance: mailing_models.Mailing, validated_data: OrderedDict) -> mailing_models.Mailing:
        app.control.revoke(task_id=instance.task_id, terminate=True, signal="SIGKILL")
        instance = super().update(instance, validated_data)
        instance = polls_services.mailing_task_creator_and_task_id_updator(instance)

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