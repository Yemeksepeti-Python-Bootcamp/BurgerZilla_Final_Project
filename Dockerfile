
FROM python:3.9-alpine

RUN apk update
RUN apk add py-pip
RUN apk add gcc musl-dev python3-dev libffi-dev libressl-dev cargo
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN python3 -m venv env

RUN apk add build-base
RUN apk add --no-cache supervisor

RUN env/bin/python -m pip install --upgrade pip
RUN env/bin/pip install -r requirements.txt

COPY app app
COPY run.py config.py .env boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 5000

ENTRYPOINT ["sh","boot.sh"]