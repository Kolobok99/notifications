from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers

from apps.api import views

router = routers.DefaultRouter()

router.register(r'client', views.ClientAPIView, basename='client')
router.register(r'tag', views.ClientTagWithoutUpdateAPIView, basename='tag')
router.register(r'mailing', views.MailingAPIView, basename='mailing')


urlpatterns = router.urls

urlpatterns += [
    path('statistic/', views.MailingStatisticListAPIView.as_view())
]

urlpatterns += [
    path('docs/', TemplateView.as_view(template_name="swagger.html")),
]