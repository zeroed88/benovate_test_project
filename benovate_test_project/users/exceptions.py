from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if response.data.get('detail'):
            response.data['message'] = response.data['detail']
        if response.data.get('non_field_errors'):
            response.data['message'] = response.data['non_field_errors'][0]

    return response
