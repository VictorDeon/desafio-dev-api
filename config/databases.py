from decouple import config

POSTGRES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_DB', default="bycoders-db"),
        'USER': config('POSTGRES_USER', default="bycoders"),
        'PASSWORD': config('POSTGRES_PASSWORD', default="bycoders"),
        'HOST': config('POSTGRES_HOST', default="postgres"),
        'PORT': "5432"
    }
}

DATABASES = POSTGRES
