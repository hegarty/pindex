import yaml
import boto3
import logging

# load yml file to dictionary
credentials = yaml.load(open('./credentials.yml'))

# access values from dictionary
username = credentials['database']['username']


def _connect_s3(jw_config):
    """
        Creates a boto3 client from 
        @type jw_config: jwplayer.config.AppConfig object
        @param jw_config: AppConfig object with aws config variables
        @rtype: boto3.session.Session.client
        @return: boto3.session.Session.client, boto3 client
    """
    logging.info('Attempting to connect to s3')
    session = boto3.session.Session(
        region_name=jw_config.aws.region,
        aws_access_key_id=jw_config.aws.key,
        aws_secret_access_key=jw_config.aws.secret
    )
    return session.client('s3', config=boto3.session.Config(signature_version='s3v4'))


