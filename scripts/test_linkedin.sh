#!/bin/bash

# Load .env file
if [ ! -f .env ]; then
    echo ".env file not found"
    exit 1
fi

source .env

# Construct the parameter overrides
PARAM_OVERRIDES="LinkedInSecretArn=$LINKEDIN_SECRET_ARN TwitterConsumerKeyArn=$TWITTER_CONSUMER_KEY_ARN TwitterConsumerKeySecretArn=$TWITTER_CONSUMER_KEY_SECRET_ARN TwitterAccessTokenArn=$TWITTER_ACCESS_TOKEN_ARN TwitterAccessTokenSecretArn=$TWITTER_ACCESS_TOKEN_SECRET_ARN"

# Run the SAM command
echo '{"url": "https://www.brettcooke.io/posts/syndicating-this-blog-part-i"}' | sam local invoke --debug --event - "LinkedInPosterFunction" --parameter-overrides $PARAM_OVERRIDES
