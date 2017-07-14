FROM python:3

MAINTAINER Alexandre Gama <alexandre.gama.lima@gmail.com>

RUN apt-get update \
    && apt-get install -y vim \
    && apt-get install -y jq

RUN pip3 install boto3
