from django.urls import path, include
from rest_framework import routers

from . import views


app_name = 'upload'
router = routers.DefaultRouter()


router.register(r'upload-files', views.UploadViewSet, basename='upload_files')


urlpatterns = [
    path('', include(router.urls)),
]
