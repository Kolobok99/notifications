import re

from django.utils import timezone
from rest_framework import serializers

from services.services import get_value_from_validate_data_or_instance


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


class ClientTagValidator:
    """
        Валидатор ClientTagSerializer.tag

        Args:
            tag (ClientTag.tag): тэг

        Поверяет, что код не содержит пробелов
    """

    def __init__(self, tag):
        self.__call__(tag)

    def __call__(self, tag):
        errors = {}

        if ' ' in tag:
            errors['error_tag_spaces'] = "ошибка: тэг не содержит пробелов!"

        if errors:
            raise serializers.ValidationError(errors)


class MailingStartTimeValidator:
    """
        Валидатор MailingSerializer

        Args:
            start_time (Mailing.start_time): время начала рассылки
            end_time (Mailing.end_time): время завершения рассылки

        Поверяет, что время начала рассылки не превышает время завершения
    """

    requires_context = True

    def __init__(self, data, serializer):
        self.__call__(data, serializer)

    def __call__(self, data, serializer):

        errors = {}

        start_time = get_value_from_validate_data_or_instance(serializer.instance, data, 'start_time')
        end_time = get_value_from_validate_data_or_instance(serializer.instance, data, 'end_time')

        if start_time > end_time:
            errors['start_time > end_time'] = f"ошибка: время начала > времени конца"

        if errors:
            raise serializers.ValidationError(errors)


class MailingEndTimeValidator:
    """
        Валидатор MailingSerializer

        Args:
            current_time (datetime): текущее время
            end_time (Mailing.end_time): время завершения рассылки

        Поверяет, что время текущее время не превышает время завершения
    """

    requires_context = True

    def __init__(self, data, serializer):
        self.__call__(data, serializer)

    def __call__(self, data, serializer):

        errors = {}
        current_time = timezone.now()

        end_time = get_value_from_validate_data_or_instance(serializer.instance, data, 'end_time')

        if current_time > end_time:
            errors['current_time > end_time'] = f"ошибка: текущее время > времени конца"

        if errors:
            raise serializers.ValidationError(errors)


class MailingTimeIntervalValidator:
    """
        Валидатор MailingSerializer

        Args:
            time_interval_start (Mailing.time_interval_start): начала временного интервала
            time_interval_end (Mailing.time_interval_end): конец временного интервала

        Если переданы оба значения, проверяет, что конец не превышает начала интервала
    """

    requires_context = True

    def __init__(self, data, serializer):
        self.__call__(data, serializer)

    def __call__(self, data, serializer):
        errors = {}

        time_interval_start = get_value_from_validate_data_or_instance(serializer.instance, data, 'time_interval_start')
        time_interval_end = get_value_from_validate_data_or_instance(serializer.instance, data, 'time_interval_end')

        if (time_interval_start and time_interval_end) and (time_interval_start > time_interval_end):
            errors['error_time_interval'] = f"ошибка: неккоректное время временного интервала"

        if errors:
            raise serializers.ValidationError(errors)