FROM python:3.8.3-alpine

WORKDIR /usr/src/loog

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN apk add py-cryptography
RUN apk add gcc musl-dev libffi-dev openssl-dev python3-dev zlib-dev jpeg-dev
RUN apk add build-base mysql-dev bash cargo

RUN pip install -r requirements/production.txt

COPY ./entrypoint.sh ./entrypoint.sh
COPY . .

RUN chmod +x ./entrypoint.sh

