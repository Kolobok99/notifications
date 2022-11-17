from django.db.models import Model
from typing import OrderedDict


def get_value_from_validate_data_or_instance(instance: Model, data: OrderedDict, key: str):
    """
        Пытается получить значение из cловаря data по ключу key
        Если key нет в data.keys(), пытается получить значение атрибута key из instance
        Если такого аргуента нет, возвращает None

        Args:
            instance (Model): инстанс любой модели
            data (Dict): validated_data
            key (str): ключ по которому ищут значение в data/instance
        Returns
            data[key] / instance.key / None

    """

    value = data.get(key, getattr(instance, key, None))

    return value
