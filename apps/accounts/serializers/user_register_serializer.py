from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema_serializer
from .user_serializer import UserSerializer
from shared.exception import LivreException

User = get_user_model()


@extend_schema_serializer(exclude_fields=["deleted"])
class UserRegisterSerializer(UserSerializer):
    """
    Dados de autenticação do usuário.
    """

    password = serializers.CharField(
        label="Senha de acesso",
        help_text="Senha de acesso aos sistemas.",
        error_messages={
            "required": "A senha do usuário é obrigatório.",
            "blank": "A senha do usuário não pode está vazio."
        },
        write_only=True
    )

    confirm_password = serializers.CharField(
        label="Confirmação de Senha",
        help_text="Confirmaçao da senha de acesso aos sistemas.",
        error_messages={
            "required": "A confirmação da senha do usuário é obrigatório.",
            "blank": "A confirmação da senha do usuário não pode está vazio."
        },
        write_only=True
    )

    def validate(self, attributes):
        """
        Valida os dados de entrada.
        """

        if attributes.get('password') != attributes.get('confirm_password'):
            raise LivreException("As senhas não combinam.", status_code=status.HTTP_400_BAD_REQUEST)

        return attributes

    def create(self, validated_data):
        """
        Cria um usuário.
        """

        return User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
