from common.reset_response.custom_pagination import LargeResultsSetPagination


class BasePagination(LargeResultsSetPagination):
    """
    分页器
    """
    page_size = 20
    page_size_query_param = 'page-size'
    page_query_param = "page"
    max_page_size = 100
