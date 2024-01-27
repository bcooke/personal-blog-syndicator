import boto3
import os
import requests
from bs4 import BeautifulSoup
import tweepy
from botocore.exceptions import ClientError
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

def lambda_handler(event, context):
    try:
        url = event.get('url')
        success, message = post_to_twitter(url)
        if success:
            return {'statusCode': 200, 'body': "Successfully posted to Twitter!"}
        else:
            return {'statusCode': 500, 'body': message}
    except Exception as e:
        logger.error("Error in Lambda Handler: ", exc_info=True)
        return {'statusCode': 500, 'body': f"Lambda Handler Error: {str(e)}"}

def fetch_metadata(url):
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
            return True, {'title': title, 'description': description}
        else:
            return False, {'error': 'Failed to retrieve webpage metadata'}
    except Exception as e:
        return False, {'error': str(e)}

def post_to_twitter(url):
    try:
        consumer_key = get_secret('TWITTER_CONSUMER_KEY_ARN')
        consumer_secret = get_secret('TWITTER_CONSUMER_KEY_SECRET_ARN')
        access_token = get_secret('TWITTER_ACCESS_TOKEN_ARN')
        access_token_secret = get_secret('TWITTER_ACCESS_TOKEN_SECRET_ARN')

        client = tweepy.Client(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret
        )

        success, metadata = fetch_metadata(url)
        if not success:
            logger.error(f"Metadata fetch failed: {metadata.get('error')}")
            return False, metadata.get('error')

        title = metadata.get('title')
        description = metadata.get('description')

        if title or description:
            tweet_text = f"{title}\n\n{url}" if title else f"Check out this link: {url}"
            response = client.create_tweet(text=tweet_text)

            if response:
                tweet_url = f"https://twitter.com/user/status/{response.data['id']}"
                logger.info(f"Tweet posted successfully: {tweet_url}")
                return True, None

        logger.error("Failed to post tweet: Empty title and description")
        return False, "Failed to post tweet: Empty title and description"

    except Exception as e:
        logger.error("Error posting to Twitter: ", exc_info=True)
        return False, str(e)

def get_secret(name):
    secret_arn = os.environ[name]
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_arn)
        return get_secret_value_response['SecretString']
    except ClientError as e:
        logger.error("Error retrieving secret: ", exc_info=True)
        raise e  # Rethrowing the exception after logging
