from rest_framework import routers

from apps.api import views

router = routers.DefaultRouter()

router.register(r'client', views.ClientAPIView, basename='client')
router.register(r'tag', views.ClientTagWithoutUpdateAPIView, basename='tag')
