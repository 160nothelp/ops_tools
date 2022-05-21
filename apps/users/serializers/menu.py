from rest_framework import serializers

from users.models import MenuModel


class MenuLv3Serializer(serializers.ModelSerializer):
    class Meta:
        model = MenuModel
        fields = '__all__'


class MenuLv2Serializer(serializers.ModelSerializer):
    children = MenuLv3Serializer(many=True)

    class Meta:
        model = MenuModel
        fields = ('id',
                  'children',
                  'title',
                  'parent',
                  'menu_type',
                  'code',
                  'icon',
                  'curl',
                  'hidden',
                  'redirect',
                  'active_menu',
                  'create_time')


class MenuSerializer(serializers.ModelSerializer):
    children = MenuLv2Serializer(many=True)

    class Meta:
        model = MenuModel
        fields = ('id',
                  'children',
                  'title',
                  'parent',
                  'menu_type',
                  'code',
                  'icon',
                  'curl',
                  'hidden',
                  'redirect',
                  'active_menu',
                  'create_time')





