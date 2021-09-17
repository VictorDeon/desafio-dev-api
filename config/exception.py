from rest_framework.views import exception_handler
from rest_framework.serializers import ValidationError


def custom_exception_handler(exc, context):
    """
    Customiza as exceções do Django Rest Framework.
    """

    response = exception_handler(exc, context)

    if response is None:
        raise exc

    data = {'detail': response.data.get('detail', '')}

    if isinstance(exc, ValidationError):
        for key in response.data:
            result = response.data[key]
            while not isinstance(result, list):
                for key in result:
                    result = result[key]

            data['detail'] = result[0]

    if response is not None:
        response.data = data

    return response
