import yaml
import os
import boto3
import logging

from boto3.session import Session
#from pprint import pprint

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


session = Session(aws_access_key_id = creds['aws']['AWSAccessKeyId'],aws_secret_access_key = creds['aws']['AWSSecretKey'])
#s3 = session.resource('s3')
#your_bucket = s3.Bucket('shredly/photos')


#for s3_file in your_bucket.objects.all():
#    for key in s3_file
#   print(s3_file.key)

prefix = "stamps/"
s3 = session.resource('s3')
bucket = s3.Bucket(name="shredly")

for obj in bucket.objects.filter(Prefix=prefix):
    # print('{1}'.format(bucket.name, obj.key))
    print(obj)
