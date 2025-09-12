# Code used to get data from the New York Times API

#%% 

# Imports

import json
import requests
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

#%%

# Function to get NY Times API Key from the Secrets Manager

def get_secret():

    secret_name = "nytimes-api-key"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']

    return secret
#%%

# Lambda function

def lambda_handler(event, context):

    # Get stories from the NY Times API
    api_key = json.loads(get_secret())['nytimes-api-key']
    response = requests.get(f'https://api.nytimes.com/svc/topstories/v2/home.json?api-key={api_key}')
    payload = response.json()['results']

    # Adds an ref_date info into each register
    for story in payload:
        story['ref_date'] = datetime.now().strftime('%Y-%m-%d')

    # Saving file to S3
    s3 = boto3.client('s3')
    file_content = json.dumps(payload)
    bucket_name = 'tmw-lagodomago-nytimes-raw'
    file_key = f'top_stories/{datetime.now().strftime("%Y-%m-%d")}.json'
    
    s3.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=file_content
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Stories have been saved to S3 successfully ')
    }
