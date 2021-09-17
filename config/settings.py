# flake8: noqa
from .envs import *
from .apps import INSTALLED_APPS
from .databases import DATABASES
from .middleware import MIDDLEWARE
from .password import AUTH_PASSWORD_VALIDATORS
from .templates import TEMPLATES
from .internationalization import *
from .rest import *
from .files import *
from decouple import config

DEBUG = config('ENVIRONMENT', default="development") == "development"

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

ALLOWED_HOSTS = ['*']

if os.environ['ENVIRONMENT'] == 'development':
    CORS_ORIGIN_ALLOW_ALL = True
else:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"https:\/\/(([a-zA-Z]|[-_])+\.)?bycoders((\.com\.br)|(\.com))$",
    ]
