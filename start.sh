#!/bin/bash

echo "Espera o POSTGRESQL inicializar e insere as variáveis de ambiente"
postgres_ready() {
python3 << END
import sys
import psycopg2
import os
try:
    psycopg2.connect(
      dbname=os.environ.get("POSTGRES_DB", "bycoders-db"),
      user=os.environ.get("POSTGRES_USER", "bycoders"),
      password=os.environ.get("POSTGRES_PASSWORD", "bycoders"),
      host=os.environ.get("POSTGRES_HOST", "postgres"),
      port=5432
    )
except psycopg2.OperationalError as error:
    print(error)
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgresql não está acessivel - Espere..."
  sleep 1
done

echo "Criando as migrações e inserindo no banco de dados PostgreSQL"
python3 manage.py makemigrations
python3 manage.py migrate

echo "Rodando o servidor"
gunicorn config.wsgi --bind 0.0.0.0:8000 --reload --graceful-timeout=900 --timeout=900 --workers 1
