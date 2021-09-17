import datetime


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'config.exception.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}


SIMPLE_JWT = {
    # Tempo de expiração do token: 1 dia
    # Quando expirado, precisamos obter outro token
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',)
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'ByCoders CNAB API',
    'DESCRIPTION': 'API do desafio ByCoders',
    'VERSION': '0.1.0'
}


AUTH_USER_MODEL = 'accounts.User'
