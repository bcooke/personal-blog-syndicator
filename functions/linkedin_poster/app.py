import boto3
import os
from botocore.exceptions import ClientError
from linkedin_api.clients.restli.client import RestliClient



def lambda_handler(event, context):
    url = event.get('url')
    post_to_linkedin(url)


def get_three_legged_access_token():
    secret_arn = os.environ['LINKED_IN_SECRET_ARN']
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_arn
        )
    except ClientError as e:
        raise e

    access_token = get_secret_value_response['SecretString']
    return access_token


def post_to_linkedin(url):
    restli_client = RestliClient()
    access_token = get_three_legged_access_token()
    response = restli_client.get(
        resource_path="/userinfo",
        access_token=access_token
    )
    print(response.entity)
    return response.entity
