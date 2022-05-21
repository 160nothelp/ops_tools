from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        # response.data.clear()
        response.data['code'] = response.status_code
        # response.data['data'] = []

        if response.status_code == 404:
            try:
                response.data['message'] = response.data.pop('detail')
                response.data['message'] = "未找到结果"
            except KeyError:
                response.data['message'] = "未找到结果"

        if response.status_code == 400:
            if response.data.get('message'):
                pass
            else:
                response.data['message'] = '提交参数错误'

        elif response.status_code == 401:
            response.data['message'] = "身份验证失败"

        elif response.status_code >= 500:
            response.data['message'] = "Internal service errors"

        elif response.status_code == 403:
            response.data['message'] = "Access denied"

        elif response.status_code == 405:
            response.data['message'] = 'Request method error'
        response.code = response.status_code
        response.status_code = 200
    return response
