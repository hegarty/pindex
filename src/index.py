import yaml
import os
import boto3
import logging
import json
import time

from boto3.session import Session
#from pprint import pprint

# load yml file to dictionary
s = os.path.dirname(__file__)
f = os.path.join(s, 'conf.d/secret.yaml')
creds = yaml.load(open(f))

aws_k = creds['aws']['AWSAccessKeyId'] 
aws_s = creds['aws']['AWSSecretKey']

#Init S3 client and return a list of all obejcts in referenced bucket
bucket = 'pindex908'
prefix = ''
s3_host = 'https://s3.amazonaws.com/'
s3_client = boto3.client('s3',aws_access_key_id = aws_k, aws_secret_access_key = aws_s, region_name='us-east-1')
s3_res = s3_client.list_objects(Bucket = bucket,Prefix = prefix)

rkg_client = boto3.client('rekognition',aws_access_key_id = aws_k,aws_secret_access_key = aws_s,region_name='us-east-1')

ddb_client = boto3.resource('dynamodb',aws_access_key_id = aws_k,aws_secret_access_key = aws_s,region_name='us-east-1')


def ddb(meta):
	print('meta: ', json.dumps(meta))
	'''
	table = ddb_client.Table('r_test')
	table.put_item(
	Item={
		'resource': resource_url,
		'labels': labels,
		'age_range': age_range,
		'emotions': emotions
		})
	'''

def get_filename(f):
	n = f['Key'].rsplit('/', 1)
	print ('FILE: '+s3_host+bucket+'/'+n[0],"---",repr(time.time()))
	return n[0]

def get_meta():
	meta = {"resource_url":"none","labels":[],"emotions":[]}

	for f in s3_res['Contents']:
		time.sleep(1)
		filename = get_filename(f)
		meta['resource_url'] = s3_host+bucket+'/'+filename
		rkg_res = rkg_client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':filename}},MinConfidence=98)

		for label in rkg_res['Labels']:
			meta['labels'].append(label['Name'])

		res = rkg_client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':filename}},Attributes=['ALL'])
		for face_detail in res['FaceDetails']:
			meta['age_range'] = face_detail['AgeRange']

			for emt in face_detail['Emotions']:
				if not emt['Type'] in meta['emotions']:
					meta['emotions'].append(emt['Type'])

		ddb(meta)
get_meta()
