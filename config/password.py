# Eles são validadores de senhas para criar senhas fortes no sistema
password_validation = 'django.contrib.auth.password_validation'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': f'{password_validation}.UserAttributeSimilarityValidator'},
    {'NAME': f'{password_validation}.MinimumLengthValidator'},
    {'NAME': f'{password_validation}.CommonPasswordValidator'},
    {'NAME': f'{password_validation}.NumericPasswordValidator'},
]
