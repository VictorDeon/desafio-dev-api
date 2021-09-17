from .exception import GenericException
from rest_framework.views import status
import re


class RegexValidator:
    """
    Validador de Regex
    """

    def __init__(self, regex, message=None):
        """
        Construtor
        """

        self.regex = regex
        self.message = message

    def __call__(self, value):
        """
        Validação.
        """

        pattern = re.match(self.regex, value, re.IGNORECASE)

        if not pattern:
            if self.message:
                raise LivreException(self.message, status_code=status.HTTP_400_BAD_REQUEST)
            else:
                raise LivreException(f"{value} não está no formato correto.", status_code=status.HTTP_400_BAD_REQUEST)
