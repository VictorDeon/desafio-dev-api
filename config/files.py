from decouple import config
from pathlib import Path
import os

# Crie caminhos dentro do projeto como este: /config/files.py
BASE_DIR = Path(__file__).resolve().parent

# O caminho absoluto para os arquivos estáticos coletados
# Ex: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Prefixo da URL para arquivos estáticos
# Ex: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# O caminho absoluto para os arquivos dinâmicos coletados
# Ex: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Prefixo da URL para arquivos dinâmicos
# Ex: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'
