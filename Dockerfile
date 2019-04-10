FROM python:3.4-alpine
#COPY  /src/conf.d/credentials ~/.aws/credentials
WORKDIR /Users/terencehegarty/projects/pindex/worker

RUN apk update
RUN apk add build-base
RUN apk add jpeg-dev
RUN apk add zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

ENV PYTHONUNBUFFERED 1

RUN pip install pillow

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
#COPY . /tests
#WORKDIR /worker/src
CMD ["python", "./src/index.py"]

