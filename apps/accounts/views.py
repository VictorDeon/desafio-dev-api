from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.views import status
from rest_framework.response import Response
from shared.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .permissions import CreateListUserPermission, UpdateOwnProfile
from . import serializers

User = get_user_model()


@extend_schema_view(
    list=extend_schema(exclude=True),
    retrieve=extend_schema(exclude=True),
    create=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
    destroy=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
    current_user=extend_schema(exclude=True)
)
class UserViewSet(ModelViewSet):
    """
    CRUD de usuários
    """

    def get_queryset(self):
        """
        Gerencia a lista de usuários.
        """

        email = self.request.query_params.get('email', None)
        queryset = User.objects.all()

        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset

    def get_serializer_class(self):
        """
        Retorna a classe de serialização de acordo com o tipo
        de ação disparado.

        ações: list, create, destroy, retrieve, update, partial_update
        """

        if self.action == 'list' or self.action == 'create':
            return serializers.UserRegisterSerializer
        else:
            return serializers.UserSerializer

    def get_permissions(self):
        """
        Pega as permissões de determinada ação.
        """

        if self.action == 'list' or self.action == 'create':
            permission_classes = (CreateListUserPermission,)
        elif self.action == 'current_user':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (UpdateOwnProfile,)

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path="current-user", url_name="current-user")
    def current_user(self, request):
        """
        Pega o usuário autenticado.
        """

        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
