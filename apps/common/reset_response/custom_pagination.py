from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response


class LargeResultsSetPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        code = 20000
        msg = 'success'
        if not data:
            code = 404
            msg = "Data Not Found"

        return Response(OrderedDict([
            ('code', code),
            ('message', msg),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
        ]))

