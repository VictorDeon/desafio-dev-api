install:
	# Instala uma nova dependência
	docker-compose exec web pip3 install ${package}

remove:
	# Remove um pacote
	docker-compose exec web pip3 uninstall ${package}

requirements:
	# Verifica todas as dependências
	docker-compose exec web pip3 freeze

bash:
	# Entrar dentro do container
	docker-compose exec web bash

logs:
	# Visualiza os logs
	docker-compose logs -ft web

# DATABASE -----------------------------------------------------

migrations:
	# Cria todas as migrações
	docker-compose exec web python3 manage.py makemigrations

migrate:
	# Rodas as migrações no banco de dados
	docker-compose exec web python3 manage.py migrate

show_migrations:
	# Mostra todas as migrações de um app
	docker-compose exec web python3 manage.py showmigrations ${app}

undo_migrate:
	# Reverter uma ou mais migrações
	docker-compose exec web python3 manage.py migrate ${app} ${migration}

fix_migrations:
	# Arrumar migrações
	docker-compose exec web python3 manage.py makemigrations --merge

shell:
	# Roda o shell do django
	docker-compose exec web python3 manage.py shell

dbshell:
	# Entrar no database do banco de dados
	docker-compose exec web python3 manage.py dbshell

superuser:
	# Cria um superusuário
	docker-compose exec web python3 manage.py createsuperuser

# QUALITY -----------------------------------------------------

path := apps

flake8:
	# Roda o flake8
	docker-compose exec web flake8 . --count

test:
	# Roda todos os testes
	docker-compose exec web coverage run --source='.' manage.py test apps.cnab.tests --keepdb

report:
	# Gera o relatório de testes
	docker-compose exec web coverage report

html:
	# Gera o relatório em html
	docker-compose exec web coverage html
