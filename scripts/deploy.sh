#!/bin/bash

# Load .env file
if [ ! -f .env ]; then
    echo ".env file not found"
    exit 1
fi

source .env

# Construct the parameter overrides
PARAM_OVERRIDES="ParameterKey=LinkedInSecretArn,ParameterValue=$LINKEDIN_SECRET_ARN \
ParameterKey=TwitterConsumerKeyArn,ParameterValue=$TWITTER_CONSUMER_KEY_ARN \
ParameterKey=TwitterConsumerKeySecretArn,ParameterValue=$TWITTER_CONSUMER_KEY_SECRET_ARN \
ParameterKey=TwitterAccessTokenArn,ParameterValue=$TWITTER_ACCESS_TOKEN_ARN \
ParameterKey=TwitterAccessTokenSecretArn,ParameterValue=$TWITTER_ACCESS_TOKEN_SECRET_ARN"

# Run the SAM deploy command
sam deploy --parameter-overrides $PARAM_OVERRIDES
