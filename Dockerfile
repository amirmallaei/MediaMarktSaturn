FROM python:3.9.16-bullseye

LABEL maintainer="Amir Mallaei <amirmallaei@gmail.com>"

ENV PYTHONUNBUFFERED 1
ENV DJANGO_CONFIGURATION Docker
ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /src
COPY ./src /src
WORKDIR /src/


RUN apt-get update -y && apt-get install -y gcc ghostscript
RUN pip install --upgrade pip


RUN pip install -r requierments.txt
