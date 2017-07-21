FROM python:3.4-alpine
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
#CMD ["python", "app.py"]

