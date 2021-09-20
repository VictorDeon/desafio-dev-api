from rest_framework.permissions import BasePermission
from rest_framework.views import status
from shared.permissions import is_logged
from shared.exception import GenericException


class RetrieveLoggedPermission(BasePermission):
    """
    Permissão para pegar os dados de um usuário autenticado.
    """

    def has_permission(self, request, view):
        """
        Verifica se o usuário tem permissão de ver os dados solicitados.
        """

        if not is_logged(request):
            raise GenericException("Usuário precisa esta autenticado para realizar essa ação!", status_code=status.HTTP_401_UNAUTHORIZED)

        return True
