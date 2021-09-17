from rest_framework.exceptions import APIException
from rest_framework.views import status


class GenericException(APIException):
    """
    Exceção genérica da livre.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Ocorreu um erro desconhecido."
    default_code = "error"

    def __init__(self, detail=None, status_code=None):
        """
        Construtor.
        """

        if status_code:
            self.status_code = status_code

        super(GenericException, self).__init__(detail=detail, code=self.default_code)
