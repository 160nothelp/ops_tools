from rest_framework import serializers
from upload.models import UploadModel


class UploadSerializer(serializers.ModelSerializer):
    username = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UploadModel
        fields = '__all__'
