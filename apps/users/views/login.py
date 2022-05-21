from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator

from users.serializers import MyTokenObtainPairSerializer
from common.token_verification import TokenGetUserObj


class MyTokenObtainPairView(TokenObtainPairView):
    """
    登录token
    """
    serializer_class = MyTokenObtainPairSerializer


class GetUserInfoView(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    userInfo
    """
    permission_classes = (IsAuthenticated, )

    @method_decorator(TokenGetUserObj)
    def list(self, request, *args, **kwargs):

        user_obj = request.user_obj
        data = {'name': user_obj.username, 'avatar': user_obj.avatar, 'user_id': user_obj.id,
                'roles': [i.title for i in list(user_obj.role.all())], "introduction": user_obj.introduction}
        if len(data.get('roles')) <= 0:
            data.get('roles').append('test')
        re_data = {"data": data,
                   "code": 20000,
                   "message": "success"
                   }
        return Response(re_data, status=status.HTTP_200_OK)
