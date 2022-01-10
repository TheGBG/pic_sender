import logging
import sys
import os


LOG_CONFIG = {
    'name': 'event-tracker',
    'level': logging.DEBUG,
    'stream_handler': logging.StreamHandler(sys.stdout),
    'format': '%(asctime)s: %(module)s: %(levelname)s: %(message)s'
}

GLOBAL_CONFIG =  {
    'image_folder': 'images',
    'media_folder': 'media',
    'expendable_images_folder': os.path.join('images', 'expendable_level'),
}

TWITTER_CONFIG = {
    'api_key': os.environ["TWITTER_API_KEY"],
    'api_secret': os.environ["TWITTER_API_KEY_SECRET"],
    'bearer_token': os.environ["TWITTER_BEARER_TOKEN"],
    'image_folder': GLOBAL_CONFIG["image_folder"]
}

REDDIT_CONFIG = {
    'client_id': os.environ["REDDIT_CLIENT_ID"],
    'client_secret': os.environ["REDDIT_CLIENT_SECRET"],
    'user_agent': os.environ["REDDIT_USER_AGENT"],
    'image_folder': GLOBAL_CONFIG["image_folder"]
}

IMAGE_MAKER_CONFIG = {
    'media_folder': GLOBAL_CONFIG["media_folder"],
    'image_folder': GLOBAL_CONFIG["image_folder"],
    'expendable_images_folder': GLOBAL_CONFIG["expendable_images_folder"]
}

TELEGRAM_CONFIG = {
    'bot_token': os.environ["TELEGRAM_BOT_TOKEN"]
}
