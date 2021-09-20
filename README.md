# Desafio programação - para vaga desenvolvedor ByCoders

Desafio CNAB

## Setup do projeto

O projeto utiliza uma arquitetura do tipo cliente-servidor na qual o servidor é uma API REST em Django Rest Framework e o cliente
é uma aplicação do tipo SPA criada em React. Foi utilizada essa arquitetura pela sua organização e separação de responsabilidades
que é um dos principais principios do SOLID.

O projeto foi dockerizado logo o mesmo tem que ser instalado.

Antes de subir a infraestrutura crie o arquivo `.env` seguindo o exemplo do arquivo `.env.example` a chave será enviada no email.

Para subir o backend API execute os seguintes comandos:

```sh
docker-compose up
```

A partir disso sua infraestrutura está criada, para realizar algum comando no docker utilize o arquivo Makefile
para facilitar a escrita dos comandos. Por exemplo:

```sh
# Se precisar executar as migrações
make migrations
make migrate

# Se precisar instalar um novo pacote dentro do docker ou remove-lo
make install package=<nome-do-pacote>
make remove package=<nome-do-pacote>

# Rodar a folha de estilo python flake8
make flake8

# Rodar os testes automatizados
make test

# Verificar a cobertura de código. (executar após a execução dos tests)
make report
```

Para conseguir enviar o arquivo de CNAB no frontend é necessário criar um usuário administrador. Com ele
você consegue se autenticar no sistema.

```sh
make superuser
```

Para acessar a documentação do projeto é só acessar a URL que será mostrada ao subir o servidor,
lá tem a documentação de todos os endpoints e autenticação.

```sh
http://0.0.0.0:8000/
```

No **github actions** é possível visualizar o flake8 e os testes sendo rodados.

## Produção

Criar o github actions para o deploy continuo em algum servidor. Ex: AWS

Se quiser subir a API em produção pode inserir a imagem em na AWS Docker Registry e utiliza-la em um orquestrador de container
kubernetes EKS da AWS, ou subir em uma função lambda da AWS por meio de um serverless. Já o frontend é só subir na AWS Amplify.
