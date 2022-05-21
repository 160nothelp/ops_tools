from rest_framework.permissions import IsAuthenticated

from common.reset_response.custom_viewset_base import CustomViewBase
from common.base_class.base_pagination import BasePagination


class BaseViewSet(CustomViewBase):
    permission_classes = (IsAuthenticated,)
    pagination_class = BasePagination
