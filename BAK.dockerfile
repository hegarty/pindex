FROM ubuntu:14.04

MAINTAINER Terence

# Install Python.
RUN \
apt-get update && \
apt-get install -y python python-dev python-pip python-virtualenv python-flask

#RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

#ENV DEV_PINDEX
RUN pip install -r requirements.txt
