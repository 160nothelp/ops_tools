from common.base_class.base_view import BaseViewSet
from ops.models import FgcBitopImgAliossUpdateTaskModel, MkAliossUpdateTaskModel, SidAliossUpdateTaskModel
from ops.serializers import FgcBitopImgAliossUpdateTaskSerializer, MkAliossUpdateSerializer, SidAliossUpdateSerializer


class FgcBitopImgAliossUpdateTaskView(BaseViewSet):
    queryset = FgcBitopImgAliossUpdateTaskModel.objects.all().order_by('-create_time')
    serializer_class = FgcBitopImgAliossUpdateTaskSerializer
    http_method_names = ('get', 'post')
    search_fields = ('img_url',)


class MkAliossUpdateView(BaseViewSet):
    queryset = MkAliossUpdateTaskModel.objects.all().order_by('-create_time')
    serializer_class = MkAliossUpdateSerializer
    http_method_names = ('get', 'post')
    search_fields = ('img_url',)


class SidAliossUpdateView(BaseViewSet):
    queryset = SidAliossUpdateTaskModel.objects.all().order_by('-create_time')
    serializer_class = SidAliossUpdateSerializer
    http_method_names = ('get', 'post')
    search_fields = ('img_url',)

