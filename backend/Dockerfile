FROM python:3.9-alpine AS build-env

# set environment varibles
ENV LANG=es_CO.UTF-8
ENV LC_ALL=es_CO.UTF-8
ENV LC_CTYPE=es_CO.UTF8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

RUN apk add --no-cache tzdata
ENV TZ America/Bogota


RUN apk --update add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq \
    # pillow dependencies
    jpeg-dev \
    zlib-dev

ARG requirements
COPY ./requirements /tmp/requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/$requirements


FROM build-env
WORKDIR /app
COPY ./ /app
EXPOSE 8000
