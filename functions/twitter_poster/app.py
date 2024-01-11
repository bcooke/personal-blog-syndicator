import boto3
import os
from botocore.exceptions import ClientError
import tweepy


def lambda_handler(event, context):
    url = event.get('url')
    post_to_twitter(url)


def post_to_twitter(url):
    consumer_key = get_secret('TWITTER_CONSUMER_KEY_ARN')
    consumer_secret = get_secret('TWITTER_CONSUMER_KEY_SECRET_ARN')
    access_token = get_secret('TWITTER_ACCESS_TOKEN_ARN')
    access_token_secret = get_secret('TWITTER_ACCESS_TOKEN_SECRET_ARN')

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    response = client.create_tweet(
        text="This Tweet was Tweeted using Tweepy and Twitter API v2!"
    )
    print(f"https://twitter.com/user/status/{response.data['id']}")


def get_secret(name):
    secret_arn = os.environ[name]
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

    secret = get_secret_value_response['SecretString']
    return secret