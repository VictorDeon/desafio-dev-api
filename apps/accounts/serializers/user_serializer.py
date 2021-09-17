from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from drf_spectacular.utils import extend_schema_serializer
from shared.validators import RegexValidator

User = get_user_model()


@extend_schema_serializer(exclude_fields=["deleted"])
class UserSerializer(serializers.Serializer):
    """
    Dados de autenticação do usuário.
    """

    id = serializers.IntegerField(
        label="Identificador",
        help_text="Identificador único do usuário.",
        read_only=True
    )

    name = serializers.CharField(
        label="Nome",
        help_text="Nome completo do usuário.",
        error_messages={
            "required": "O nome do usuário é obrigatório.",
            "blank": "O nome do usuário não pode está vazio."
        }
    )

    email = serializers.EmailField(
        label="Email",
        help_text="Email de autenticação do usuário.",
        error_messages={
            "required": "O email do usuário é obrigatório.",
            "blank": "O email do usuário não pode está vazio."
        },
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Já existe um usuário com esse email"
            ),
            RegexValidator(
                regex=r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
                message="O campo email não está no formato correto."
            )
        ]
    )

    short_name = serializers.CharField(
        label="Nome e Sobrenome",
        help_text="Nome e Sobrenome do usuário",
        required=False,
        read_only=True
    )

    deleted = serializers.BooleanField(
        required=False,
        label="Usuário deletado?",
        help_text="Verifica se o usuário foi removido do sistema",
        write_only=True
    )

    def update(self, instance, validated_data):
        """
        Atualiza um usuário.
        """

        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.deleted = validated_data.get('deleted', instance.deleted)
        instance.save()

        return instance

    def to_representation(self, instance):
        """
        Formata os dados de saída no modo leitura
        """

        return {
            "name": instance.name,
            "email": instance.email,
            "short_name": instance.short_name,
            "is_superuser": instance.is_superuser,
            "is_admin": instance.is_staff
        }
