import logging
import sys
import os


LOG_CONFIG = {
    'name': 'event-tracker',
    'level': logging.DEBUG,
    'stream_handler': logging.StreamHandler(sys.stdout),
    'format': '%(asctime)s: %(module)s: %(levelname)s: %(message)s'
}

TWITTER_CONFIG = {
    'api_key': os.environ["TWITTER_API_KEY"],
    'api_secret': os.environ["TWITTER_API_KEY_SECRET"],
    'bearer_token': os.environ["TWITTER_BEARER_TOKEN"],
}

REDDIT_CONFIG = {
    'client_id': os.environ["REDDIT_CLIENT_ID"],
    'client_secret': os.environ["REDDIT_CLIENT_SECRET"],
    'user_agent': os.environ["REDDIT_USER_AGENT"]
}
