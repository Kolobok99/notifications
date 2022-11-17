import datetime

import pytest

from django.contrib.auth.models import User

from apps.mailings import models as mailings_models


@pytest.fixture()
def tags():
    tags_titles = [
        '#первый',
        '#второй',
        '#третий',
    ]

    for title in tags_titles:
        mailings_models.ClientTag.objects.create(
            tag=title
        )
    return mailings_models.ClientTag.objects.all()


@pytest.fixture()
def admin():
    admin = User.objects.create_superuser(
        username='admin',
        password='admin',
        is_active=True,
    )

    return admin


@pytest.fixture()
def region_code():
    region_code = mailings_models.RegionCode.objects.create(code='123')
    return region_code


@pytest.fixture()
def clients(tags, region_code):
    phones = [
        '71234560001',
        '71234560002',
        '71234560003',
        '71234560004',
        '71234560005',
    ]

    for phone in phones:
        client = mailings_models.Client.objects.create(phone=phone, region_code=region_code)
        client.tags.add(tags.first())
        client.tags.add(tags.last())
    return mailings_models.Client.objects.all()

@pytest.fixture()
def mailings(clients, tags, region_code):
    mailings_data = [
        {
            'start_time': '2023-01-01',
            'end_time': '2023-01-12',
            'text': 'Тестовый текст',
        },
        {
            'start_time': '2024-01-01',
            'end_time': '2024-01-12',
            'text': 'Тестовый текст (2)',
        }
    ]
    for data in mailings_data:
        m = mailings_models.Mailing.objects.create(**data)
        m.filter_tags.add(tags.first())
        m.filter_codes.add(region_code)

    return mailings_models.Mailing.objects.all()
