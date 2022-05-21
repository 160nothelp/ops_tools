from rest_framework_simplejwt import authentication


def TokenGetUserObj(fc):
    def wrapper(request):
        token = request.META.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        token_msg = authentication.JWTAuthentication().get_validated_token(token)
        user_obj = authentication.JWTAuthentication().get_user(token_msg)
        request.user_obj = user_obj
        return fc(request)
    return wrapper

