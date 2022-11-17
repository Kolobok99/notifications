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