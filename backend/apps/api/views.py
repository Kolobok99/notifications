from rest_framework import viewsets, generics

from conf.settings import logger

from apps.api import permissions
from apps.mailings import serializers as mailing_serializers
from apps.mailings import models as mailings_models


class ClientAPIView(viewsets.ModelViewSet):
    """APIView модели Client"""

    queryset = mailings_models.Client.objects.all()
    serializer_class = mailing_serializers.ClientSerializer
    lookup_field = 'phone'
    lookup_url_kwarg = 'phone'

    def destroy(self, request, *args, **kwargs):
        logger.debug(f'DESTROY <CLIENT_phone_{self.get_object().phone}>')
        return super().destroy(request, *args, **kwargs)


class ClientTagWithoutUpdateAPIView(viewsets.ModelViewSet):
    """
        APIView модели ClientTag
        (с запрещенным изменением)
    """

    queryset = mailings_models.ClientTag.objects.all()
    serializer_class = mailing_serializers.ClientTagSerializer
    http_method_names = ['head', 'options', 'get', 'post', 'delete']
    lookup_field = 'tag'


class MailingAPIView(viewsets.ModelViewSet):
    """
        APIView модели Mailing
        (с запрещенным изменением завершенных рассылок)
    """

    queryset = mailings_models.Mailing.objects.all()
    serializer_class = mailing_serializers.MailingSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [permissions.MailingUpdating]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        logger.debug(f'DESTROY <MAILING_id_{self.get_object().id}>')
        return super().destroy(request, *args, **kwargs)

class MailingStatisticListAPIView(generics.ListAPIView):
    """read_only APIView модели MailingStatistic"""

    queryset = mailings_models.MailingStatistic.objects.all()
    serializer_class = mailing_serializers.MailingStatisticSerializer