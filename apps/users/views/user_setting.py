from common.base_class.base_view import BaseViewSet
from users.serializers import UserProfileSerializer, PermissionSerializer, RoleSerializer
from users.models import UserProfile, PermissionModel, RoleModel


class UserProfileView(BaseViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')


class PermissionView(BaseViewSet):
    queryset = PermissionModel.objects.all()
    serializer_class = PermissionSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')


class RoleView(BaseViewSet):
    queryset = RoleModel.objects.all()
    serializer_class = RoleSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')

