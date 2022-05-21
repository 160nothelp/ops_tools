from django.urls import path, include
from rest_framework import routers

from . import views


app_name = 'domains'
router = routers.DefaultRouter()


router.register(r'mind-domain', views.CfMindDomainView, basename='cf_mind_domain')
router.register(r'ssl-cert', views.SslCertView, basename='ssl_cert')


urlpatterns = [
    path('', include(router.urls)),
    path('server-mind-domain-monitor', views.ServerMindDomainMonitorView.as_view())
]
