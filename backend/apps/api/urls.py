from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

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
    path('base-auth/', include('rest_framework.urls')),
    path('token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


urlpatterns += [
    path('docs/', TemplateView.as_view(template_name="swagger.html")),
]