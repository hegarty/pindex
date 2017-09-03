import yaml
import os
import boto3
import logging
import json

from boto3.session import Session

# load yml file to dictionary
s = os.path.dirname(__file__)
f = os.path.join(s, 'conf.d/secret.yaml')
creds = yaml.load(open(f))

#def _connect_s3():
	#Creates a boto3 client from 
   	#@type jw_config: jwplayer.config.AppConfig object
  	#@param jw_config: AppConfig object with aws config variables
   	#@rtype: boto3.session.Session.client
   	#@return: boto3.session.Session.client, boto3 client

   	#session = boto3.session.Session(
   	#region_name = 'us_east_1',
   	#aws_access_key_id = creds['aws']['AWSAccessKeyId'],
   	#aws_secret_access_key = creds['aws']['AWSSecretKey']
   	#)

   	#return session.client('s3', config=boto3.session.Config(signature_version='s3v4'))


session = Session(aws_access_key_id = creds['aws']['AWSAccessKeyId'],
                  aws_secret_access_key = creds['aws']['AWSSecretKey'])
s3 = session.resource('s3')
your_bucket = s3.Bucket('pindex908')

for s3_file in your_bucket.objects.all():
    print(s3_file.key)

#Labels
if __name__ == "__main__":
    fileName='surprised.jpg'
    bucket='pindex908'

    client=boto3.client('rekognition',
  	aws_access_key_id = creds['aws']['AWSAccessKeyId'],
    aws_secret_access_key = creds['aws']['AWSSecretKey'],
	region_name='us-east-1')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}},MinConfidence=75)

    print('Detected labels for ' + fileName)
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))

#Detect Faces
if __name__ == "__main__":
    #fileName='input.jpg'
    #bucket='bucket'
    #client=boto3.client('rekognition')

    response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':fileName}},Attributes=['ALL'])

    print('Detected faces for ' + fileName)
    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        print('Here are the other attributes:')
        print(json.dumps(faceDetail, indent=4, sort_keys=True))



