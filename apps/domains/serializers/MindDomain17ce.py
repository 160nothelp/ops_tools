from rest_framework import serializers

from domains.models import CloudFlareDnsParseRecordsListModel, MindDomainMonitor


class MindDomainMonitorSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='get_title_display')

    class Meta:
        model = MindDomainMonitor
        fields = '__all__'


class CfDomainRecordsSerializer(serializers.ModelSerializer):
    statusOfServer = MindDomainMonitorSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = CloudFlareDnsParseRecordsListModel
        fields = ('id',
                  'cf_records_id',
                  'cf_records_type',
                  'cf_records_name',
                  'cf_records_content',
                  'cf_records_proxiable',
                  'cf_records_proxied',
                  'cf_records_ttl',
                  'cf_mind_domain',
                  'cf_records_zone_name',
                  'cf_records_created_on',
                  'cf_records_modified_on',
                  'editing',
                  'create_time',
                  'update_time',
                  'isMonitor',
                  'statusOfServer')



