from rest_framework import serializers, validators

from apps.mailings import models as mailing_models
from apps.mailings import validators as mailing_custom_validators

from services import mailings_services


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