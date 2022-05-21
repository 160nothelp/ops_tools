import hashlib
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from common.base_class.base_view import BaseViewSet

from domains.serializers import CfDomainRecordsSerializer
from domains.models import CloudFlareDnsParseRecordsListModel, MindDomainMonitor


class CfMindDomainView(BaseViewSet):
    queryset = CloudFlareDnsParseRecordsListModel.objects.all()
    serializer_class = CfDomainRecordsSerializer
    http_method_names = ('get', 'patch')


class ServerMindDomainMonitorView(APIView):
    token_ha = hashlib.md5()
    token_ha.update(settings.SECRET_KEY.encode(encoding='utf-8'))

    def get(self, request):
        token = request.query_params.get('token')
        if token == self.token_ha.hexdigest():
            mindDomains = CloudFlareDnsParseRecordsListModel.objects.all()
            domains = [{'id': i.id, 'domain': i.cf_records_name, 'ip': i.cf_records_content} for i in mindDomains]
            return Response({'domains': domains}, status=200)
        return Response(status=403)

    def post(self, request):
        token = request.data.get('token')
        if token == self.token_ha.hexdigest():
            MindDomainMonitor.objects.update_or_create(
                title=request.data.get('title'),
                Record=CloudFlareDnsParseRecordsListModel.objects.get(id=request.data.get('id')),
                defaults={
                    'title': request.data.get('title'),
                    'Record': CloudFlareDnsParseRecordsListModel.objects.get(id=request.data.get('id')),
                    'HttpCode': request.data.get('status_code'),
                    'TotalTime': request.data.get('total_seconds')
                }
            )
            return Response(status=201)
        return Response(status=403)


