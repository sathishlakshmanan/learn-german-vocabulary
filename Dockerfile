FROM ubuntu:22.04

ENV PYTHONUNBUFFERED 1

ENV DEBIAN_FRONTEND=noninteractive

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY requirements.txt requirements.txt

USER root

RUN apt-get update \
    && apt-get install -y python3-pip python3-dev default-libmysqlclient-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt --no-cache-dir

USER 1001

COPY . /app
