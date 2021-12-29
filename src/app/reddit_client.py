import praw
import os
import requests
from app.utils import get_random_string
from app.logger_client import LoggerClient


class RedditClient():
    def __init__(self, config: dict, logger: LoggerClient, url: str):
        """
        Initializes the client for Reddit

        Args:
            config (dict): dictionary containing the keys. Comes from config.
                At the same time, config keys must be set as environment variables
            logger (LoggerClient): instance of the logger
            url (str): link to the reddit post
        """
        self._url = url
        self._config = config.REDDIT_CONFIG
        self._logger = logger

        self._reddit_client = praw.Reddit(
            client_id=self._config['client_id'],
            client_secret=self._config['client_secret'],
            user_agent=self._config['user_agent']
        )
    
    def download_image(
        self,
        image_name: str = None,
        image_folder: str = 'images',
        image_format: str = '.jpg'
    ):
        """
        Downloads and save the image harvested from the reddit post

        Arguments
        ---------
            - image_name: (str, optional): name for the image. When `None`, a
              random string will be set as name.

            - image_folder (str, optional): where to store the images.
              Defaults to 'images'.

            - image_format (str, optional): defaults to '.jpg'.
        """
        if self._url is None:
            self._logger.error('No URL found.')

        post = self._reddit_client.submission(url=self._url)
        image_url = post.url        
        requested_image = requests.get(image_url)
        
        # Ensure that we're getting response 200
        if not requested_image.ok:
            self._logger.error(f'Request not completed: {requested_image}')

        if image_name is None:
            image_name = get_random_string()

        image_filename = f'{image_name}{image_format}' 
        image_path = os.path.join(image_folder, image_filename)
        
        with open(image_path, 'wb') as f:
            f.write(requested_image.content)
            f.close()
        
        self._logger.info(f'Image saved at {image_path}')
