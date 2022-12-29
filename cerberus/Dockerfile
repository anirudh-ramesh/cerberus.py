ARG PYTHON_VERSION=3.11.0

FROM python:${PYTHON_VERSION}

MAINTAINER Anirudh Ramesh

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /goodenough

COPY requirements.txt /goodenough/

RUN pip install -r requirements.txt

COPY . /goodenough/