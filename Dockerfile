# Baixa a imagem do debian com o python:3.8
FROM python:3.6

# Remove o delay do log
ENV PYTHONUNBUFFERED 1

# Instala as dependências do sistema operacional
RUN apt-get update && apt-get install -y vim

# Cria a pasta do projeto
RUN mkdir /software

# Faz a pasta /software ser a diretorio atual
WORKDIR /software

# Adiciona os arquivo requirements.txt na pasta /software
ADD ./requirements.txt /software

# Instala as dependências do software.
RUN pip install --upgrade pip && pip3 install -r requirements.txt

# Insere todo o projeto dentro da pasta software
ADD . /software

# Expoẽ a porta 8000
EXPOSE 8000

RUN chmod +x ./start.sh

CMD ["./start.sh"]