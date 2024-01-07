import json
from datetime import datetime, timedelta
import feedparser


RSS_FEED_URL = "https://www.brettcooke.io/rss.xml"

def lambda_handler(event, context):
    blog_url = check_rss_feed(RSS_FEED_URL)
    return {
        'statusCode': 200,
        'body': json.dumps({'url': blog_url})
    }

def check_rss_feed(url):
    """
    Check an RSS feed for posts in the past 24 hours.

    Args:
    url (str): The URL of the RSS feed.

    Returns:
    str or None: The URL of the most recent post if there are any in the past 24 hours, else None.
    """
    # Parse the RSS feed
    feed = feedparser.parse(url)

    # Get the current time
    current_time = datetime.now()

    # Check for posts in the last 24 hours
    for entry in feed.entries:
        # Parse the published time of the post
        published_time = datetime(*entry.published_parsed[:6])

        # Check if the post is within the last 24 hours
        # if current_time - published_time < timedelta(days=1):
        if current_time - published_time < timedelta(hours=1):
            return entry.link

    return None
