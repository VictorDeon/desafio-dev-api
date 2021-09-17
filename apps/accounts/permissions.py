from rest_framework.permissions import BasePermission
from rest_framework.views import status
from shared.permissions import is_admin, is_logged, is_owner
from shared.exception import GenericException


class UpdateOwnProfile(BasePermission):
    """
    Permite que o usuário atualize seu próprio perfil.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check user is trying to edit their own profile.
        """

        if not is_logged(request):
            raise GenericException("Usuário não autenticado!", status_code=status.HTTP_401_UNAUTHORIZED)

        if is_admin(request):
            return True

        if not is_owner(request, obj):
            raise GenericException("Usuário não tem autorização para realizar essa ação!", status_code=status.HTTP_401_UNAUTHORIZED)

        return True


class CreateListUserPermission(BasePermission):
    """
    Permite criar um usuário somente se tiver autenticado e
    for um administrador.
    """

    def has_permission(self, request, view):
        """
        Permissões.
        """

        if is_logged(request) and is_admin(request):
            return True

        raise GenericException("Usuário não tem autorização para realizar essa ação!", status_code=status.HTTP_401_UNAUTHORIZED)
