import datetime

import pytest
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils.serializer_helpers import ReturnDict

from apps.mailings import models as mailing_models

from tests.test_api.base import BaseTestAPIClass

@pytest.mark.django_db
class TestClientAPIViewSet(BaseTestAPIClass):
    client = APIClient()
    base_path_name = 'client'

    valid_data = {
        'phone': '70001234455',
        'timezone': 0,
        'tags': ['#первый']
    }

    in_valid_data = {
        'phone': '8asda1231231',
        'tags': ['#НЕ_ТЭГ']
    }

    # ------------------------ LIST ------------------------#

    def test_list_client_by_anonymous_user(self):
        """Тест: отправка list-запроса на client от анонимного пользователя"""

        self._test_list__by_anonymous_user(self.base_path_name)

    def test_list_client_by_admin(self, admin, clients):
        """Тест: отправка list-запроса на client от админа"""

        self._test_list__by_privileged_user(admin, self.base_path_name, clients.count())

    # ------------------------ RETRIEVE ------------------------#

    def test_retrieve_client_with_valid_url_kwargs_by_anonymous_user(self, clients):
        """Тест: отправка retrieve-запроса на client с valid_url_kwargs от анонимного пользователя"""

        instance = clients.first()
        valid_url_kwargs = dict(phone=instance.phone)
        self._test_retrieve__with_valid_url_kwarg_by_anonymous_user(self.base_path_name, valid_url_kwargs)

    def test_retrieve_client_with_valid_url_kwargs_by_admin(self, clients, admin):
        """Тест: отправка retrieve-запроса на client с valid_url_kwargs от админа"""

        instance = clients.first()
        valid_url_kwarg = dict(phone=instance.phone)

        data = self._test_retrieve__with_valid_url_kwarg_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_url_kwarg=valid_url_kwarg,
            instance=instance,
            standard_fields=['id', 'phone', 'timezone']
        )
        client_tags = instance.tags.all()
        assert data['tags'][0] == client_tags.first().tag
        assert data['tags'][-1] == client_tags.last().tag



    # ------------------------ CREATE ------------------------#

    def test_create_client_with_valid_data_by_anonymous_user(self, clients, admin):
        """Тест: отправка create-запроса на client с valid_data от анонимного пользователя"""

        self._test_create__with_valid_data_by_anonymous_user(self.base_path_name, self.valid_data)

    def test_create_client_with_valid_data_and_new_region_code_by_admin(self, clients, admin, region_code):
        """Тест: отправка create-запроса на client с valid_data и new_region_code от админа """

        valid_data = self.valid_data.copy()
        valid_data['phone'] = '7' + region_code.code[::-1] + valid_data['phone'][4:]
        region_code_start_count = mailing_models.RegionCode.objects.count()

        self._test_create__with_valid_payload_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_payload=valid_data,
            model=mailing_models.Client,
            start_count=clients.count()
        )

        instance = mailing_models.Client.objects.get(phone=valid_data['phone'])
        instance_tags = instance.tags.all()
        assert valid_data['phone'] == instance.phone
        assert valid_data['timezone'] == instance.timezone
        assert valid_data['phone'][1:4] == instance.region_code.code
        assert mailing_models.RegionCode.objects.count() == region_code_start_count + 1
        assert valid_data['tags'][0] == instance_tags.first().tag


    def test_create_client_with_valid_data_and_old_region_code_by_admin(self, clients, admin, region_code):
        """Тест: отправка create-запроса на client с valid_data и old_region_code от админа """

        valid_data = self.valid_data.copy()
        valid_data['phone'] = '7' + region_code.code + valid_data['phone'][4:]
        region_code_start_count = mailing_models.RegionCode.objects.count()

        self._test_create__with_valid_payload_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_payload=valid_data,
            model=mailing_models.Client,
            start_count=clients.count()
        )

        instance = mailing_models.Client.objects.get(phone=valid_data['phone'])
        instance_tags = instance.tags.all()
        assert valid_data['phone'] == instance.phone
        assert valid_data['timezone'] == instance.timezone
        assert valid_data['phone'][1:4] == instance.region_code.code
        assert mailing_models.RegionCode.objects.count() == region_code_start_count
        assert valid_data['tags'][0] == instance_tags.first().tag


    def test_create_client_with_IN_valid_data_by_admin(self, clients, admin, region_code):
        """Тест: отправка create-запроса на client с in_valid_data от админа """

        phone_error = 'error_phone_format'

        data = self._test_create__with_IN_valid_payload_by_privileged_user(prv_user=admin,
                                                                           base_path_name=self.base_path_name,
                                                                           in_valid_payload=self.in_valid_data,
                                                                           model=mailing_models.Client,
                                                                           start_count=clients.count())

        assert phone_error in data['phone'].keys()
        assert 'does_not_exist' == data['tags'][0].code

    def test_create_client_with_IN_valid_used_phone_by_admin(self, clients, admin, region_code):
        """Тест: отправка create-запроса на client с in_valid_data от admin"""

        in_valid_data = self.in_valid_data.copy()
        in_valid_data['phone'] = clients.first().phone

        data = self._test_create__with_IN_valid_payload_by_privileged_user(prv_user=admin,
                                                                           base_path_name=self.base_path_name,
                                                                           in_valid_payload=in_valid_data,
                                                                           model=mailing_models.Client,
                                                                           start_count=clients.count())

        assert 'unique' == data['phone'][0].code

    # ------------------------ UPDATE ------------------------#

    def test_update_client_with_valid_data_by_anonymous_user(self, clients):
        instance = clients.first()
        valid_url_kwargs = dict(phone=instance.phone)

        self._test_update__with_valid_payload_by_anonymous_user(
            base_path_name=self.base_path_name,
            valid_url_kwargs=valid_url_kwargs,
            valid_payload=self.valid_data
        )

    def test_update_client_with_valid_data_and_new_region_code_by_admin(self, clients, admin, region_code):
        """Тест: отправка update-запроса на client с valid_data и new_region_code от админа """

        instance = clients.first()
        valid_url_kwargs = dict(phone=instance.phone)

        valid_data = self.valid_data.copy()
        valid_data['phone'] = '7' + region_code.code[::-1] + valid_data['phone'][4:]
        region_code_start_count = mailing_models.RegionCode.objects.count()

        self._test_update__with_valid_data_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_url_kwargs=valid_url_kwargs,
            valid_payload=valid_data,
            model=mailing_models.Client,
            start_count=clients.count()
        )

        instance = mailing_models.Client.objects.get(phone=valid_data['phone'])
        instance_tags = instance.tags.all()
        assert valid_data['phone'] == instance.phone
        assert valid_data['timezone'] == instance.timezone
        assert valid_data['phone'][1:4] == instance.region_code.code
        assert mailing_models.RegionCode.objects.count() == region_code_start_count + 1
        assert valid_data['tags'][0] == instance_tags.first().tag

    def test_update_client_with_valid_data_and_old_region_code_by_admin(self, clients, admin, region_code):
        """Тест: отправка update-запроса на client с valid_data и old_region_code от админа """

        instance = clients.first()
        valid_url_kwargs = dict(phone=instance.phone)

        valid_data = self.valid_data.copy()
        valid_data['phone'] = '7' + region_code.code + valid_data['phone'][4:]
        region_code_start_count = mailing_models.RegionCode.objects.count()

        self._test_update__with_valid_data_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_url_kwargs=valid_url_kwargs,
            valid_payload=valid_data,
            model=mailing_models.Client,
            start_count=clients.count()
        )

        instance = mailing_models.Client.objects.get(phone=valid_data['phone'])
        instance_tags = instance.tags.all()
        assert valid_data['phone'] == instance.phone
        assert valid_data['timezone'] == instance.timezone
        assert valid_data['phone'][1:4] == instance.region_code.code
        assert mailing_models.RegionCode.objects.count() == region_code_start_count
        assert valid_data['tags'][0] == instance_tags.first().tag

    def test_update_client_with_IN_valid_data_by_admin(self, clients, admin, region_code):
        """Тест: отправка update-запроса на client с in_valid_data от админа """

        instance = clients.last()
        valid_url_kwargs = dict(phone=instance.phone)

        phone_error = 'error_phone_format'
        data = self._test_update__with_IN_valid_payload_by_privileged_user(prv_user=admin,
                                                                           base_path_name=self.base_path_name,
                                                                           valid_url_kwargs=valid_url_kwargs,
                                                                           in_valid_payload=self.in_valid_data,
                                                                           model=mailing_models.Client,
                                                                           instance=instance,
                                                                           )

        assert phone_error in data['phone'].keys()
        assert 'does_not_exist' == data['tags'][0].code

    def test_update_client_with_IN_valid_used_phone_by_admin(self, clients, admin, region_code):
        """Тест: отправка update-запроса на client с in_valid_data от admin"""

        instance = clients.last()
        valid_url_kwargs = dict(phone=instance.phone)
        in_valid_data = self.in_valid_data.copy()
        in_valid_data['phone'] = clients.first().phone

        data = self._test_update__with_IN_valid_payload_by_privileged_user(prv_user=admin,
                                                                           base_path_name=self.base_path_name,
                                                                           valid_url_kwargs=valid_url_kwargs,
                                                                           in_valid_payload=in_valid_data,
                                                                           model=mailing_models.Client,
                                                                           instance=instance,
                                                                           )

        assert 'unique' == data['phone'][0].code

    # ------------------------ DELETE ------------------------#

    def test_delete_client_by_anonymous_user(self, clients):
        """Тест: отправка delete-запроса на client по valid_url_kwargs от анонимного пользователя"""

        instance = clients.last()
        valid_url_kwargs = dict(phone=instance.phone)

        self._test_delete__with_valid_url_kwargs_by_anonymous_user(
            self.base_path_name, valid_url_kwargs
        )

    def test_delete_client_valid_url_kwargs_by_manager(self, admin, clients):
        """Тест: отправка delete-запроса на client по valid_url_kwargs от админа"""

        instance = clients.last()
        valid_url_kwargs = dict(phone=instance.phone)
        count = clients.count()

        self._test_delete__with_valid_url_kwargs_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_url_kwargs=valid_url_kwargs,
            instance=instance,
            count=count
        )


@pytest.mark.django_db
class TestTagAPIViewSet(BaseTestAPIClass):
    client = APIClient()
    base_path_name = 'tag'

    valid_data = {
        'tag': '#новый',
    }

    in_valid_data = {
        'tag': 'НЕ ТЭГ!!!',
    }

    # ------------------------ LIST ------------------------#

    def test_list_tag_by_anonymous_user(self):
        """Тест: отправка list-запроса на tag от анонимного пользователя"""

        self._test_list__by_anonymous_user(self.base_path_name)

    def test_list_tag_by_admin(self, admin, tags):
        """Тест: отправка list-запроса на tag от админа"""

        self._test_list__by_privileged_user(admin, self.base_path_name, tags.count())

    # ------------------------ RETRIEVE ------------------------#

    def test_retrieve_tag_with_valid_url_kwargs_by_anonymous_user(self, tags):
        """Тест: отправка retrieve-запроса на tag с valid_url_kwargs от анонимного пользователя"""

        instance = tags.first()
        valid_url_kwargs = dict(tag=instance.tag)
        self._test_retrieve__with_valid_url_kwarg_by_anonymous_user(self.base_path_name, valid_url_kwargs)

    def test_retrieve_tag_with_valid_url_kwargs_by_admin(self, tags, admin):
        """Тест: отправка retrieve-запроса на tag с valid_url_kwargs от админа"""

        instance = tags.first()
        valid_url_kwarg = dict(tag=instance.tag)

        data = self._test_retrieve__with_valid_url_kwarg_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_url_kwarg=valid_url_kwarg,
            instance=instance,
            standard_fields=['tag']
        )




    # ------------------------ CREATE ------------------------#

    def test_create_tag_with_valid_data_by_anonymous_user(self, tags, admin):
        """Тест: отправка create-запроса на tag с valid_data от анонимного пользователя"""

        self._test_create__with_valid_data_by_anonymous_user(self.base_path_name, self.valid_data)

    def test_create_tag_with_valid_data_by_admin(self, tags, admin):
        """Тест: отправка create-запроса на tag с valid_data от админа """


        self._test_create__with_valid_payload_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_payload=self.valid_data,
            model=mailing_models.ClientTag,
            start_count=tags.count()
        )

        instance = mailing_models.ClientTag.objects.get(tag=self.valid_data['tag'])
        assert self.valid_data['tag'] == instance.tag


    def test_create_tag_with_IN_valid_data_by_admin(self, tags, admin):
        """Тест: отправка create-запроса на tag с in_valid_data от админа """

        error_tag_spaces = 'error_tag_spaces'

        data = self._test_create__with_IN_valid_payload_by_privileged_user(prv_user=admin,
                                                                           base_path_name=self.base_path_name,
                                                                           in_valid_payload=self.in_valid_data,
                                                                           model=mailing_models.ClientTag,
                                                                           start_count=tags.count())

        assert error_tag_spaces in data['tag'].keys()

    # ------------------------ UPDATE ------------------------#

    def test_update_tag_with_valid_data_by_anonymous_user(self, tags):
        """Тест: отправка update-запроса на tag с valid_data от анонимного пользователя"""

        instance = tags.first()
        valid_url_kwargs = dict(tag=instance.tag)

        self._test_update__with_valid_payload_by_anonymous_user(
            base_path_name=self.base_path_name,
            valid_url_kwargs=valid_url_kwargs,
            valid_payload=self.valid_data
        )

    def test_forbidden_update_tag_with_valid_data_by_admin(self, tags, admin):
        """Тест: отправка forbidden update-запроса на tag с valid_data от админа """

        instance = tags.first()
        valid_url_kwargs = dict(tag=instance.tag)
        error_code = 'method_not_allowed'

        self.client.force_login(admin)
        url = reverse(f'{self.base_path_name}-detail', kwargs=valid_url_kwargs)

        response = self.client.patch(url, data=self.valid_data, format='json')

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.data['detail'].code == error_code


    # ------------------------ DELETE ------------------------#

    def test_delete_tag_by_anonymous_user(self, tags):
        """Тест: отправка delete-запроса на tag по valid_url_kwargs от анонимного пользователя"""

        instance = tags.last()
        valid_url_kwargs = dict(tag=instance.tag)

        self._test_delete__with_valid_url_kwargs_by_anonymous_user(
            self.base_path_name, valid_url_kwargs
        )

    def test_delete_tag_valid_url_kwargs_by_manager(self, admin, tags):
        """Тест: отправка delete-запроса на tag по valid_url_kwargs от админа"""

        instance = tags.last()
        valid_url_kwargs = dict(tag=instance.tag)
        count = tags.count()

        self._test_delete__with_valid_url_kwargs_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_url_kwargs=valid_url_kwargs,
            instance=instance,
            count=count
        )


@pytest.mark.django_db
class TestMailingAPIViewSet(BaseTestAPIClass):
    client = APIClient()
    base_path_name = 'mailing'

    valid_data = {
        'start_time': '2023-12-12T12:00',
        'end_time': '2024-12-12T12:00',
        'text': 'Тестовый valid text',
        'filter_tags': ['#первый'],
        'filter_codes': ['123'],
    }

    in_valid_data = {
        'start_time': '2022-12-12T12:00',
        'end_time': '2021-12-12T12:00',
        'text': 'Тестовый valid text',
        'filter_tags': ['#NOT_TAG'],
        'filter_codes': ['000'],
    }

    # ------------------------ LIST ------------------------#

    def test_list_mailing_by_anonymous_user(self):
        """Тест: отправка list-запроса на mailing от анонимного пользователя"""

        self._test_list__by_anonymous_user(self.base_path_name)

    def test_list_mailing_by_admin(self, admin, mailings):
        """Тест: отправка list-запроса на mailing от админа"""

        self._test_list__by_privileged_user(admin, self.base_path_name, mailings.count())

    # ------------------------ RETRIEVE ------------------------#

    def test_retrieve_mailing_with_valid_url_kwargs_by_anonymous_user(self, mailings):
        """Тест: отправка retrieve-запроса на mailing с valid_url_kwargs от анонимного пользователя"""

        instance = mailings.first()
        valid_url_kwargs = dict(pk=instance.pk)
        self._test_retrieve__with_valid_url_kwarg_by_anonymous_user(self.base_path_name, valid_url_kwargs)

    def test_retrieve_mailing_with_valid_url_kwargs_by_admin(self, mailings, tags, region_code, admin):
        """Тест: отправка retrieve-запроса на mailing с valid_url_kwargs от админа"""

        instance = mailings.first()
        valid_url_kwarg = dict(pk=instance.pk)

        data = self._test_retrieve__with_valid_url_kwarg_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_url_kwarg=valid_url_kwarg,
            instance=instance,
            standard_fields=['id', 'text']
        )
        mailing_tags = instance.filter_tags.all()
        mailing_codes = instance.filter_codes.all()

        assert data['filter_tags'][0] == mailing_tags.first().tag
        assert data['filter_codes'][0] == mailing_codes.first().code
        assert data['time_interval_start'] == '00:00:00'
        assert data['time_interval_end'] == '23:59:00'
        assert data['statistic'] is None



    # ------------------------ CREATE ------------------------#

    def test_create_mailing_with_valid_data_by_anonymous_user(self, mailings, admin):
        """Тест: отправка create-запроса на mailing с valid_data от анонимного пользователя"""

        self._test_create__with_valid_data_by_anonymous_user(self.base_path_name, self.valid_data)

    def test_create_mailing_with_valid_data_by_admin(self, mailings, admin):
        """Тест: отправка create-запроса на mailing с valid_data от админа """

        valid_data = self.valid_data.copy()

        data = self._test_create__with_valid_payload_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_payload=valid_data,
            model=mailing_models.Mailing,
            start_count=mailings.count()
        )
        instance = mailing_models.Mailing.objects.get(text=valid_data['text'])
        instance_tags = instance.filter_tags.all()
        instance_codes = instance.filter_codes.all()

        assert valid_data['filter_tags'][0] == instance_tags.first().tag
        assert valid_data['filter_codes'][0] == instance_codes.first().code
        assert datetime.time(hour=0, minute=0) == instance.time_interval_start
        assert datetime.time(hour=23, minute=59) == instance.time_interval_end

        assert valid_data['start_time'] == (instance.start_time + datetime.timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M')
        assert valid_data['end_time'] == (instance.end_time + datetime.timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M')


    def test_create_mailing_with_IN_valid_data_by_admin(self, mailings, admin):
        """Тест: отправка create-запроса на client с in_valid_data от админа """

        current_time_more_end_time = 'current_time > end_time'
        start_time_more_end_time = 'start_time > end_time'

        data = self._test_create__with_IN_valid_payload_by_privileged_user(prv_user=admin,
                                                                           base_path_name=self.base_path_name,
                                                                           in_valid_payload=self.in_valid_data,
                                                                           model=mailing_models.Mailing,
                                                                           start_count=mailings.count())

        assert 'does_not_exist' == data['filter_tags'][0].code
        assert 'does_not_exist' == data['filter_codes'][0].code



    # ------------------------ UPDATE ------------------------#

    def test_update_mailing_with_valid_data_by_anonymous_user(self, mailings):
        instance = mailings.first()
        valid_url_kwargs = dict(pk=instance.pk)

        self._test_update__with_valid_payload_by_anonymous_user(
            base_path_name=self.base_path_name,
            valid_url_kwargs=valid_url_kwargs,
            valid_payload=self.valid_data
        )

    def test_update_client_with_valid_data_and_new_region_code_by_admin(self, mailings, admin):
        """Тест: отправка update-запроса на mailing (status = C) с valid_data от админа """

        instance = mailings.first()
        valid_url_kwargs = dict(pk=instance.pk)

        valid_data = self.valid_data.copy()

        self._test_update__with_valid_data_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_url_kwargs=valid_url_kwargs,
            valid_payload=valid_data,
            model=mailing_models.Mailing,
            start_count=mailings.count()
        )

        instance = mailing_models.Mailing.objects.get(text=valid_data['text'])
        instance_tags = instance.filter_tags.all()
        instance_codes = instance.filter_codes.all()

        assert valid_data['text'] == instance.text
        assert valid_data['filter_tags'][0] == instance_tags.first().tag
        assert valid_data['filter_codes'][0] == instance_codes.first().code

        assert valid_data['start_time'] == (instance.start_time + datetime.timedelta(hours=3)).strftime(
            '%Y-%m-%dT%H:%M')
        assert valid_data['end_time'] == (instance.end_time + datetime.timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M')

    def test_update_mailings_with_IN_valid_data_by_admin(self, admin, mailings):
        """Тест: отправка update-запроса на mailings с in_valid_data от админа """

        instance = mailings.last()
        valid_url_kwargs = dict(pk=instance.pk)

        data = self._test_update__with_IN_valid_payload_by_privileged_user(prv_user=admin,
                                                                           base_path_name=self.base_path_name,
                                                                           valid_url_kwargs=valid_url_kwargs,
                                                                           in_valid_payload=self.in_valid_data,
                                                                           model=mailing_models.Mailing,
                                                                           instance=instance,
                                                                           )

        assert 'does_not_exist' == data['filter_tags'][0].code
        assert 'does_not_exist' == data['filter_codes'][0].code

    @pytest.mark.parametrize(
        "status",
        ['S', 'F'],
    )
    def test_update_started_and_finished_mailings_is_prohibited_by_admin(self,admin, mailings, status):
        """Тест: отправка ЗАПРЕЩЕННОГО update запроса к STARTED/FINISHED mailing от админа"""
        instance = mailings.last()
        instance.status = status
        instance.save()

        valid_url_kwargs = dict(pk=instance.pk)


        self._test_update__with_valid_payload_by_UN_privileged_user(
            un_prv_user=admin,
            base_path_name=self.base_path_name,
            valid_url_kwargs=valid_url_kwargs,
            valid_payload=self.valid_data
        )

    # ------------------------ DELETE ------------------------#

    def test_delete_mailing_by_anonymous_user(self, mailings):
        """Тест: отправка delete-запроса на mailing по valid_url_kwargs от анонимного пользователя"""

        instance = mailings.last()
        valid_url_kwargs = dict(pk=instance.pk)

        self._test_delete__with_valid_url_kwargs_by_anonymous_user(
            self.base_path_name, valid_url_kwargs
        )

    @pytest.mark.parametrize(
        "status",
        ['C', 'S', 'F'],
    )
    def test_delete_mailing_valid_url_kwargs_with_status_by_manager(self, admin, mailings, status):
        """Тест: отправка delete-запроса на mailing со статусом CREATED/STARTED/FINISHED по valid_url_kwargs от админа"""

        instance = mailings.last()
        instance.status = status
        instance.save()
        valid_url_kwargs = dict(pk=instance.pk)
        count = mailings.count()

        self._test_delete__with_valid_url_kwargs_by_privileged_user(
            prv_user=admin,
            base_path_name=self.base_path_name,
            valid_url_kwargs=valid_url_kwargs,
            instance=instance,
            count=count
        )

