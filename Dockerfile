FROM python:3.4-alpine
#COPY  /src/conf.d/credentials ~/.aws/credentials
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /src
COPY . /tests
#WORKDIR /src
#CMD ["python", "./src/index.py"]

