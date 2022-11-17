import datetime

from django.db.models import DateField
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils.serializer_helpers import ReturnDict

from apps.mailings import models as mailings_models

class BaseTestAPIClass:

    client = APIClient()

    # ---------------------- ANONYMOUS ----------------------#
    def _test_request_by_anonymous_user(self, method_name, url, payload=False):
        """BaseMethod: отправка request от анонимного пользователя"""

        method = getattr(self.client, method_name)

        if payload:
            response = method(url, data=payload)
        else:
            response = method(url)

        data = response.data

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert data['detail'].code == 'not_authenticated'

    # ---------------------- UN_PRIVILEGED ----------------------#
    def _test_request_by_UN_privileged_user(self, method_name, url, payload=False):
        """BaseMethod: отправка request от не_привилегированного пользователя"""

        method = getattr(self.client, method_name)

        if payload:
            response = method(url, data=payload)
        else:
            response = method(url)
        data = response.data

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert data['detail'].code == 'permission_denied'

    # ------------------------ LIST ------------------------#
    def _test_list__by_anonymous_user(self, base_path_name):
        """BaseMethod: отправка list-запроса от анонимного пользователя"""

        url = reverse(f'{base_path_name}-list')
        self._test_request_by_anonymous_user("get", url)

    def _test_list__by_UN_privileged_user(self, un_prv_user, base_path_name):
        """BaseMethod: отправка list-запроса от не_привилегированного пользователя"""

        self.client.force_login(un_prv_user)

        url = reverse(f'{base_path_name}-list')
        self._test_request_by_UN_privileged_user("get", url)

    def _test_list__by_privileged_user(self, prv_user, base_path_name, count):
        """BaseMethod: отправка list-запроса от привилегированного пользователя"""

        self.client.force_login(prv_user)

        url = reverse(f'{base_path_name}-list')
        response = self.client.get(url)
        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert len(data) == count

        return data

# ------------------------ BASE RETRIEVE ------------------------#

    def _test_retrieve__with_valid_url_kwarg_by_anonymous_user(self, base_path_name, valid_url_kwarg):
        """BaseMethod: отправка retrieve-запроса  с valid_url_kwarg от анонимного пользователя"""

        url = reverse(f'{base_path_name}-detail', kwargs=valid_url_kwarg)
        self._test_request_by_anonymous_user('get', url)

    def _test_retrieve__with_valid_url_kwarg_by_UN_privileged_user(self, un_prv_user, base_path_name, valid_url_kwarg):
        """BaseMethod: отправка retrieve-запроса с valid_url_kwarg от un_prv_user"""

        self.client.force_login(un_prv_user)

        url = reverse(f'{base_path_name}-detail', kwargs=valid_url_kwarg)
        self._test_request_by_UN_privileged_user('get', url)

    def _test_retrieve__with_valid_url_kwarg_by_privileged_user(self, prv_user, base_path_name, valid_url_kwarg, instance, standard_fields):
        """BaseMethod: отправка retrieve-запроса на brand с valid_url_kwarg от prv_user"""

        self.client.force_login(user=prv_user)

        url = reverse(f'{base_path_name}-detail', kwargs=valid_url_kwarg)
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert type(response.data), ReturnDict

        for field in standard_fields:
            instance_field = getattr(instance, field)
            if getattr(instance_field, 'pk', None):
                instance_field = instance_field.pk
            elif type(instance_field) is datetime.date:
                instance_field = instance_field.strftime("%Y-%m-%d")
            assert instance_field == response.data[field]

        return response.data


    def _test_retrieve__with_IN_invalid_url_kwargs_by_privileged_user(self, prv_user, base_path_name, invalid_url_kwargs):
        """BaseMethod: отправка retrieve-запроса с invalid_url_kwargs от prv_user"""

        self.client.force_login(user=prv_user)

        url = reverse(f'{base_path_name}-detail', kwargs=invalid_url_kwargs)
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # ------------------------ BASE CREATE ------------------------#

    def _test_create__with_valid_data_by_anonymous_user(self, base_path_name, valid_data):
        """BaseMethod: отправка create-запроса  с valid_data от анонимного пользователя"""

        url = reverse(f'{base_path_name}-list')
        self._test_request_by_anonymous_user('post', url, payload=valid_data)

    def _test_create__with_valid_data_by_UN_privileged_user(self, un_prv_user, base_path_name, valid_data):
        """BaseMethod: отправка create-запроса с valid_data от НЕ_привилегированного пользователя"""

        self.client.force_login(un_prv_user)

        url = reverse(f'{base_path_name}-list')
        self._test_request_by_UN_privileged_user('post', url, payload=valid_data)

    def _test_create__with_valid_payload_by_privileged_user(self, prv_user, base_path_name, valid_payload, model,
                                                            start_count):
        """BaseMethod: отправка create-запроса с valid_payload от привилегированного пользователя"""

        self.client.force_login(prv_user)

        url = reverse(f'{base_path_name}-list')

        response = self.client.post(url, valid_payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert model.objects.count() == start_count + 1

        return response.data

    def _test_create__with_IN_valid_payload_by_privileged_user(self, prv_user, base_path_name, in_valid_payload, model, start_count):
        """BaseMethod: отправка create-запроса с in_valid_payload от привилегированного пользователя"""

        self.client.force_login(prv_user)

        url = reverse(f'{base_path_name}-list')

        response = self.client.post(url, in_valid_payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert model.objects.count() == start_count

        return response.data

    # ------------------------ BASE UPDATE ------------------------#

    def _test_update__with_valid_payload_by_anonymous_user(self, base_path_name, valid_url_kwargs, valid_payload):
        """BaseMethod: отправка update-запроса  с valid_payload от анонимного пользователя"""

        url = reverse(f'{base_path_name}-detail', kwargs=valid_url_kwargs)
        self._test_request_by_anonymous_user('patch', url, payload=valid_payload)

    def _test_update__with_valid_payload_by_UN_privileged_user(self, un_prv_user, base_path_name, valid_url_kwargs,
                                                               valid_payload):
        """BaseMethod: отправка update-запроса с valid_payload от НЕ_привилегированного пользователя"""

        self.client.force_login(un_prv_user)

        url = reverse(f'{base_path_name}-detail', kwargs=valid_url_kwargs)
        self._test_request_by_UN_privileged_user('patch', url, payload=valid_payload)

    def _test_update__with_valid_data_by_privileged_user(self, prv_user, base_path_name, valid_url_kwargs,
                                                         valid_payload, model, start_count):
        """BaseMethod: отправка update-запроса с valid_payload от привилегированного пользователя"""

        self.client.force_login(prv_user)

        url = reverse(f'{base_path_name}-detail', kwargs=valid_url_kwargs)

        response = self.client.patch(url, valid_payload, format='json')
        response_data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert model.objects.count() == start_count

        return response_data
        # for key in valid_payload:
        #     assert getattr(instance_after_update, key) == valid_payload[key]

    def _test_update__with_IN_valid_payload_by_privileged_user(self, prv_user, base_path_name, valid_url_kwargs,
                                                               in_valid_payload, instance, model):
        """BaseMethod: отправка update-запроса с in_valid_payload от привилегированного пользователя"""

        self.client.force_login(prv_user)

        url = reverse(f'{base_path_name}-detail', kwargs=valid_url_kwargs)

        response = self.client.patch(url, data=in_valid_payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        instance_after_update = model.objects.get(pk=instance.pk)
        fields = instance._meta.fields

        for field in fields:
            if field.name != 'modified_on':
                instance_field = getattr(instance, field.name)
                instance_after_update_field = getattr(instance_after_update, field.name)
                assert instance_after_update_field == instance_field

        return response.data




    # ------------------------ BASE DELETE ------------------------#

    def _test_delete__with_valid_url_kwargs_by_anonymous_user(self, base_path_name, valid_url_kwargs):
        """BaseMethod: отправка delete-запроса по valid_url_kwargs от анонимного пользователя"""

        url = reverse(f'{base_path_name}-detail', kwargs=valid_url_kwargs)
        self._test_request_by_anonymous_user('delete', url)

    def _test_delete__with_valid_url_kwargs_by_UN_privileged_user(self, un_prv_user, base_path_name, valid_url_kwargs):
        """BaseMethod: отправка delete-запроса по valid_url_kwargs от НЕ_привилегированного пользователя"""

        self.client.force_login(un_prv_user)

        url = reverse(f'{base_path_name}-detail', kwargs=valid_url_kwargs)
        self._test_request_by_UN_privileged_user('delete', url)

    def _test_delete__with_valid_url_kwargs_by_privileged_user(self, prv_user, base_path_name, valid_url_kwargs, instance, count):
        """BaseMethod: отправка delete-запроса по valid_url_kwargs от привилегированного пользователя"""

        self.client.force_login(user=prv_user)

        url = reverse(f'{base_path_name}-detail', kwargs=valid_url_kwargs)
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
        assert type(instance).objects.count() == count - 1
        assert type(instance).objects.filter(pk=instance.pk).count() == 0