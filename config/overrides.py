from drf_spectacular.views import SpectacularYAMLAPIView
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse, OpenApiExample
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenSerializer(TokenObtainPairSerializer):
    """
    Sobrescreve a mensagem de erro do token ao autenticar.
    """

    default_error_messages = {'no_active_account': "Nenhuma conta ativa encontrada com as credenciais fornecidas"}


class ExcludedSpectacularYAMLAPIView(SpectacularYAMLAPIView):
    """
    Remove o endpoint schema/ da documentação redoc.
    """

    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return super(ExcludedSpectacularYAMLAPIView, self).get(request, *args, **kwargs)


class TokenView(TokenObtainPairView):
    """
    Customiza a documentação do token
    """

    serializer_class = CustomTokenSerializer

    @extend_schema(
        operation_id="login JWT",
        description="Geração do token de autenticação JWT",
        tags=["Login"],
        request=inline_serializer(name="Corpo da Requisição do login", fields={
            "email": serializers.EmailField(help_text='Email de autenticação.'),
            "password": serializers.CharField(help_text='Senha de autenticação.', write_only=True)
        }),
        responses={200: OpenApiResponse(response=inline_serializer(name="Resposta login", fields={
            "access": serializers.CharField(help_text="Access token para autenticação"),
            "refresh": serializers.CharField(help_text="Refresh token para atualizar tokens expirados.")
        }), description="OK")},
        examples=[
            OpenApiExample("Exemplo request", value={"email": "user@example.com", "password": "example1234"}, request_only=True),
            OpenApiExample("Exemplo response", value={
                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.Ep5YcDX0O...",
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlb..."
            }, response_only=True)
        ]
    )
    def post(self, request, *args, **kwargs):
        """
        Documentando o endpoint de geração de token.
        """

        return super(TokenView, self).post(request, *args, **kwargs)


class AccessTokenRefreshView(TokenRefreshView):
    """
    Customiza a documentação do token refresh
    """

    @extend_schema(
        operation_id="Atualizar token",
        description="Atualização do token de autenticação JWT",
        tags=["Login"],
        request=inline_serializer(name="Corpo da Requisição do refresh token", fields={
            "refresh": serializers.CharField(help_text='Refresh token gerado.')
        }),
        responses={200: OpenApiResponse(response=inline_serializer(name="Resposta refresh token", fields={
            "access": serializers.CharField(help_text="Access token para atualizado")
        }), description="OK")},
        examples=[
            OpenApiExample("Exemplo request", value={"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlb..."}, request_only=True),
            OpenApiExample("Exemplo response", value={"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.Ep5YcDX0O..."}, response_only=True)
        ]
    )
    def post(self, request, *args, **kwargs):
        """
        Documentando o endpoint de atualização de token.
        """

        return super(AccessTokenRefreshView, self).post(request, *args, **kwargs)
