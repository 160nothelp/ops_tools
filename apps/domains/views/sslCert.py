from common.base_class.base_view import BaseViewSet

from domains.serializers import CertDirSerializer, SslCertSerializer
from domains.models import CertDirModel, SslCertModel


class SslCertView(BaseViewSet):
    queryset = SslCertModel.objects.all()
    serializer_class = SslCertSerializer
    http_method_names = ('get',)
