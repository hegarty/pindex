FROM python:3.4-alpine
#COPY  /src/conf.d/credentials ~/.aws/credentials
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
#CMD ["python", "./src/index.py"]

