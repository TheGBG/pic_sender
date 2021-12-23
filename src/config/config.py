import logging
import os
import sys


TWITTER_CONFIG = {
    'api_key': os.environ["TWITTER_API_KEY"],
    'api_secret': os.environ["TWITTER_API_KEY_SECRET"],
    'bearer_token': os.environ["TWITTER_BEARER_TOKEN"],
}