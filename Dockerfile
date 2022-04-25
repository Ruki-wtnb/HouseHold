FROM python:3.8-alpine

WORKDIR /workspace

COPY requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN apk update \
 && apk add --no-cache build-base \
 && apk add gcc mariadb-dev\
 && apk add libffi-dev \
 && apk add openssl \
 && pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \
 && apk del build-base

COPY app/main.py .

EXPOSE 8080
