from rest_framework import serializers
from django.db import transaction

from ops.models import FgcBitopImgAliossUpdateTaskModel, MkAliossUpdateTaskModel, SidAliossUpdateTaskModel, \
    UIAliossUpdateTaskModel
from ops.tasks import Fcg24ImgAliossUpdate, MkAliossUpdate, SidAliossUpdate, UIAliossUpdate
from upload.models import UploadModel


class ImgAliossUpdateTaskSerializer(serializers.ModelSerializer):
    image_file = serializers.SlugRelatedField(queryset=UploadModel.objects.all(), slug_field='id')


class FgcBitopImgAliossUpdateTaskSerializer(ImgAliossUpdateTaskSerializer):

    def create(self, validated_data):
        obj = FgcBitopImgAliossUpdateTaskModel.objects.create(**validated_data)
        transaction.on_commit(lambda: Fcg24ImgAliossUpdate.delay(obj.id))
        return obj

    class Meta:
        model = FgcBitopImgAliossUpdateTaskModel
        fields = '__all__'


class MkAliossUpdateSerializer(ImgAliossUpdateTaskSerializer):

    def create(self, validated_data):
        obj = MkAliossUpdateTaskModel.objects.create(**validated_data)
        transaction.on_commit(lambda: MkAliossUpdate.delay(obj.id))
        return obj

    class Meta:
        model = MkAliossUpdateTaskModel
        fields = '__all__'


class SidAliossUpdateSerializer(ImgAliossUpdateTaskSerializer):

    def create(self, validated_data):
        obj = SidAliossUpdateTaskModel.objects.create(**validated_data)
        transaction.on_commit(lambda: SidAliossUpdate.delay(obj.id))
        return obj

    class Meta:
        model = SidAliossUpdateTaskModel
        fields = '__all__'


class UIAliossUpdateSerializer(ImgAliossUpdateTaskSerializer):

    def create(self, validated_data):
        obj = UIAliossUpdateTaskModel.objects.create(**validated_data)
        transaction.on_commit(lambda: UIAliossUpdate.delay(obj.id))
        return obj

    class Meta:
        model = UIAliossUpdateTaskModel
        fields = '__all__'
