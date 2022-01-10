import logging
import sys
import os


LOG_CONFIG = {
    'name': 'event-tracker',
    'level': logging.DEBUG,
    'stream_handler': logging.StreamHandler(sys.stdout),
    'format': '%(asctime)s: %(module)s: %(levelname)s: %(message)s'
}

GLOBAL_CONFIG = {
    'image_folder': 'fake_image_folder'
}

TWITTER_CONFIG = {
    'api_key': 'fake_key',
    'api_secret': 'fake_secret_key',
    'bearer_token': 'fake_bearer_token',
    'image_folder': GLOBAL_CONFIG['image_folder']
}

REDDIT_CONFIG = {
    'client_id': 'fake_client_id',
    'client_secret': 'fake_client_secret',
    'user_agent': 'fake_user_agent',
    'image_folder': GLOBAL_CONFIG['image_folder']
}
