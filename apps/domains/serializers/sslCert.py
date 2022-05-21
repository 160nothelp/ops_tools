from rest_framework import serializers

from domains.models import CertDirModel, SslCertModel, CertFileModel


class CertDirSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertDirModel
        fields = '__all__'


class CertFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertFileModel
        fields = '__all__'


class SslCertSerializer(serializers.ModelSerializer):
    cert_dir = CertDirSerializer(many=True)
    cert_file = CertFileSerializer(many=True)

    class Meta:
        model = SslCertModel
        fields = '__all__'
