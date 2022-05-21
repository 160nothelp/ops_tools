from common.base_class.base_view import BaseViewSet
from .models import UploadModel
from .serializers import UploadSerializer


class UploadViewSet(BaseViewSet):
    queryset = UploadModel.objects.all()
    serializer_class = UploadSerializer
    http_method_names = ('get', 'post')
