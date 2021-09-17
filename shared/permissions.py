from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.views import status
from shared.exception import GenericException


def is_owner(request, object_user):
    """
    Vai verificar se o usuário logado é dono do objeto que será
    modificado.
    """

    return bool(object_user.id == request.user.id)


def is_read_mode(request):
    """
    Verifica se o método passado é do tipo leitura (safe methods)
    """

    if request.method in SAFE_METHODS:
        return True

    return False


def is_logged(request):
    """
    Verifica se o usuário está autenticado.
    """

    return bool(request.user and request.user.is_authenticated)


def is_admin(request):
    """
    Verifica se o usuário é administrador.
    """

    return bool(request.user and request.user.is_staff)


class IsAuthenticated(BasePermission):
    """
    Verifica se o usuário está autenticado.
    """

    def has_permission(self, request, view):
        """
        Permissão.
        """

        if not is_logged(request):
            raise GenericException("Usuário não autenticado!", status_code=status.HTTP_401_UNAUTHORIZED)

        return True


class IsAdmin(BasePermission):
    """
    Verifica se o usuário autenticado é administrador.
    """

    def has_permission(self, request, view):
        """
        Permissão.
        """

        if not is_admin(request):
            raise GenericException("Usuário não é um administrador!", status_code=status.HTTP_401_UNAUTHORIZED)

        return True
