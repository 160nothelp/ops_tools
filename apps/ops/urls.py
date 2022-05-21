from django.urls import path, include
from rest_framework import routers

from . import views


app_name = 'ops'
router = routers.DefaultRouter()


router.register(r'bitop-img-oss-update', views.FgcBitopImgAliossUpdateTaskView, basename='bitop_img_oss_update')
router.register(r'mk-img-oss-update', views.MkAliossUpdateView, basename='mk_img_oss_update')
router.register(r'sid-img-oss-update', views.SidAliossUpdateView, basename='mk_img_oss_update')


urlpatterns = [
    path('', include(router.urls)),
]
