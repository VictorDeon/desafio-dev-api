
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
