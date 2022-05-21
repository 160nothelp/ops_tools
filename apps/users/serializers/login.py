from django.utils import timezone

from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)
        return token

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
           return {
               'code': 20,
               'message': '账号密码错误'
           }

        if self.user is None or not self.user.is_active:
            return {
               'code': 20,
               'message': '账号未启用'
           }
        self.user.last_login = timezone.now()
        self.user.save()
        data = super().validate(attrs)
        re_data = dict()
        data['token'] = data['access']
        re_data['data'] = data
        re_data['code'] = 20000
        re_data['message'] = 'success'

        return re_data
