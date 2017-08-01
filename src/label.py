import yaml
import os
import boto3
import logging
import pprint
from boto3.session import Session

# load yml file to dictionary
s = os.path.dirname(__file__)
f = os.path.join(s, 'conf.d/secret.yaml')
creds = yaml.load(open(f))

#session = Session(aws_access_key_id = creds['aws']['AWSAccessKeyId'],aws_secret_access_key = creds['aws']['AWSSecretKey'])

client = boto3.client(
    'rekognition',
    region_name='us-east-1',
    aws_access_key_id=creds['aws']['AWSAccessKeyId'],
    aws_secret_access_key=creds['aws']['AWSSecretKey'],
)

print(client)

BUCKET = "hegarty_photos"
KEY = "IMG_0003.JPG"

def detect_labels(bucket, key, max_labels=10, min_confidence=90, region="us-east-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.detect_labels(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )
    return response['Labels']


for label in detect_labels(BUCKET, KEY):
    print("{Name} - {Confidence}%".format(**label))
