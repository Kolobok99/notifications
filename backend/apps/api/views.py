from rest_framework import viewsets

from apps.mailings import serializers as mailing_serializers
from apps.mailings import models as mailings_models

class ClientAPIView(viewsets.ModelViewSet):
    """APIView модели Client"""

    queryset = mailings_models.Client.objects.all()
    serializer_class = mailing_serializers.ClientSerializer
    lookup_field = 'phone'
    lookup_url_kwarg = 'phone'