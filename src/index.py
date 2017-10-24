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


def ddb(resource_url, labels, age_range, emotions):
	table = ddb_client.Table('r_test')
	table.put_item(
	Item={
		'resource': resource_url,
		'labels': labels,
		'age_range': age_range,
		'emotions': emotions
		})

def get_labels(s3_contents = s3_res['Contents']):
	for f in s3_contents:
		labels = []
		time.sleep(1)
		# Get the file name
		n = f['Key'].rsplit('/', 1)
		filename = n[0]
		print ('FILE: '+s3_host+bucket+'/'+n[0],"---",repr(time.time()))
		resource_url = s3_host+bucket+'/'+filename
		rkg_res = rkg_client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':filename}},MinConfidence=98)
		for label in rkg_res['Labels']:
			labels.append(label['Name'])

		ddb(resource_url,labels,"ok","nk")

get_labels()

'''
# Loop through each file and pull labels
for f in s3_res['Contents']:
	emotions = []
	labels = []
	time.sleep(1)
	# Get the file name
	n = f['Key'].rsplit('/', 1)
	filename = n[0]
	print ('FILE: '+s3_host+bucket+'/'+n[0],"---",repr(time.time()))
	resource_url = s3_host+bucket+'/'+filename
	rkg_res = rkg_client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':filename}},MinConfidence=98)
	for label in rkg_res['Labels']:
		labels.append(label['Name']) 

#Detect Faces
	face_res = rkg_client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':filename}},Attributes=['ALL'])
	for face_detail in face_res['FaceDetails']:
		#meta['age_range']['low'] = face_detail['AgeRange']['Low']
		#meta['age_range']['high'] = face_detail['AgeRange']['High']
		age_range = face_detail['AgeRange']
		print('Emotions: ',face_detail['Emotions'])

		for emt in face_detail['Emotions']:
			et = emt['Type']+"_"+filename
			emotions.append(et)
			print('Emotion Type: ',emt['Type'],filename)

#write to DDB
	table = ddb_client.Table('r_test')
	table.put_item(
	Item={
		'resource': resource_url,
		'labels': labels,
		'age_range': age_range,
		'emotions': emotions
		})
'''
	#print('Detected faces for ' + fn)
	#for faceDetail in response['FaceDetails']:
		#print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
		#print('Here are the other attributes:')
        
	#for key in response['FaceDetails']:
		#print(key)
		#if 'Emotions' in faceDetail: 
			#for fd in faceDetail['Emotions']:
				#print(json.dumps(fd['Type'], indent=4, sort_keys=True))
#
#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
#
#table = dynamodb.Table('Movies')
#
#title = "The Big New Movie"
#year = 2015
#
#response = table.put_item(
#   Item={
#        'year': year,
#        'title': title,
#        'info': {
#            'plot':"Nothing happens at all.",
#            'rating': decimal.Decimal(0)
#        }
#    }
#)
#
#print("PutItem succeeded:")
#


#for s3_file in your_bucket.objects.all():
#    for key in s3_file
#   print(s3_file.key)
