# Application definition
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles'
]

PROJECT_APPS = [
    'apps.accounts'
]

EXTERNAL_APPS = [
    'corsheaders',
    'drf_spectacular'
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + PROJECT_APPS
