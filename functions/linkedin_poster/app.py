import boto3
import os
import requests
from bs4 import BeautifulSoup
from botocore.exceptions import ClientError
from linkedin_api.clients.restli.client import RestliClient
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

# Constants for LinkedIn API
ME_RESOURCE = "/me"
POSTS_RESOURCE = "/posts"
API_VERSION = "202302"

def lambda_handler(event, context):
    try:
        url = event.get('url')
        success, message = post_to_linkedin(url)
        if success:
            return {'statusCode': 200, 'body': "Successfully posted to LinkedIn!"}
        else:
            return {'statusCode': 500, 'body': message}
    except Exception as e:
        logger.error("Error in Lambda Handler: ", exc_info=True)
        return {'statusCode': 500, 'body': f"Lambda Handler Error: {str(e)}"}

def get_three_legged_access_token():
    secret_arn = os.environ['LINKED_IN_SECRET_ARN']
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_arn)
    except ClientError as e:
        logger.error("Error retrieving secret: ", exc_info=True)
        raise e  # Rethrowing the exception after logging

    return get_secret_value_response['SecretString']

def fetch_metadata(url):
    logger.info(f"Fetching metadata for URL: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else ''
            description = ''
            for meta in soup.find_all('meta'):
                if 'name' in meta.attrs and meta.attrs['name'].lower() == 'description':
                    description = meta.attrs['content']
                    break
            logger.info(f"Title: {title}, Description: {description}")
            return True, {'title': title, 'description': description}
        else:
            return False, {'error': 'Failed to retrieve webpage metadata'}
    except Exception as e:
        logger.error("An error occurred while fetching metadata: ", exc_info=True)
        return False, {'error': str(e)}

def post_to_linkedin(url):
    logger.info("Posting to LinkedIn")
    try:
        restli_client = RestliClient()
        access_token = get_three_legged_access_token()
        me_response = restli_client.get(resource_path=ME_RESOURCE, access_token=access_token)

        success, metadata = fetch_metadata(url)
        if not success:
            return False, metadata.get('error')

        title = metadata.get('title')
        description = metadata.get('description')

        if title and description:
            commentary = f"{description}"
            content = {
                "article": {
                    "title": title,
                    "source": url,
                }
            }
            response = restli_client.create(
                resource_path=POSTS_RESOURCE,
                entity={
                    "author": f"urn:li:person:{me_response.entity['id']}",
                    "lifecycleState": "PUBLISHED",
                    "visibility": "PUBLIC",
                    "content": content,
                    "commentary": commentary,
                    "distribution": {
                        "feedDistribution": "MAIN_FEED",
                        "targetEntities": [],
                        "thirdPartyDistributionChannels": [],
                    },
                },
                version_string=API_VERSION,
                access_token=access_token,
            )

            if response.status_code >= 200 and response.status_code < 300:
                logger.info(f"Successfully created post: {response.entity_id}")
                return True, None
            else:
                logger.error(f"Failed to create post: {response.status_code}, {response.text}")
                return False, f"LinkedIn API Error: {response.text}"
        else:
            logger.error("No title or description available")
            return False, 'No title or description available'

    except Exception as e:
        logger.error("Error posting to LinkedIn: ", exc_info=True)
        return False, str(e)

