from rest_framework import serializers
from users.models import UserProfile, PermissionModel, RoleModel


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('username', 'date_joined', 'last_login')


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionModel
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):


    class Meta:
        model = RoleModel
        fields = '__all__'
