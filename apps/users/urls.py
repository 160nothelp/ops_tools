from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'user'
router = routers.DefaultRouter()


router.register(r'user-info', views.GetUserInfoView, basename='get_user_info')
router.register(r'user-list', views.UserProfileView, basename='set_user_list')
router.register(r'role-list', views.RoleView, basename='set_role_list')
router.register(r'menu-list', views.MenuView, basename='set_menu_list')


urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]

