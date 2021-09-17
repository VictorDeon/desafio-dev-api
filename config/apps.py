# Application definition
DJANGO_APPS = ['django.contrib.auth']

PROJECT_APPS = []

EXTERNAL_APPS = [
    'corsheaders',
    'drf_spectacular'
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + PROJECT_APPS
