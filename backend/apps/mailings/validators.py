import re

from rest_framework import serializers


class PhoneNumberValidator:
    """
        Валидатор ClientSerializer.phone

        Args:
            phone (ClientSerializer.phone): номер телефона

        Проверяет, что номер начинается с 7 и состоит из 11 цифр
    """

    def __init__(self, phone):
        self.__call__(phone)

    def __call__(self, phone):
        if not re.match(r'^7[0-9]{10}$', phone):
            raise serializers.ValidationError(
                {"error_phone_format": "ошибка: введите номер в формате 7XXXXXXXXXX"}
            )