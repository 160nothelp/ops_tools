from rest_framework import status
from common.base_class.base_view import BaseViewSet
from common.reset_response.custom_json_response import JsonResponse
from users.serializers import MenuSerializer
from users.models import MenuModel, RoleModel


class MenuView(BaseViewSet):
    queryset = MenuModel.objects.all()
    serializer_class = MenuSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        role_query = RoleModel.objects.filter(users=self.request.user)
        queryset = self.queryset.filter(roles__in=list(role_query)).distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer_data = menuDuplicate(serializer)
            return self.get_paginated_response(serializer_data)

        serializer = self.get_serializer(queryset, many=True)
        serializer_data = menuDuplicate(serializer)
        return JsonResponse(data=serializer_data, code=20000, msg="success", status=status.HTTP_200_OK)


# 根据parent_id 和 id 来去重
def menuDuplicate(serializer):
    serializer_data = list()
    for menu in serializer.data:
        if menu['parent'] is None:
            serializer_data.append(menu)
    for menu in serializer.data:
        if menu['parent']:
            if menu['parent'] not in [x['id'] for i in serializer_data for x in i['children']] and \
                    menu['parent'] not in [i['id'] for i in serializer_data]:
                serializer_data.append(menu)
    return serializer_data
