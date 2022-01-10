import praw
import os
import requests
from app.utils import extract_filename
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
        self._config = config.REDDIT_CONFIG
        self._logger = logger
        self._url = url

        self._reddit_client = praw.Reddit(
            client_id=self._config['client_id'],
            client_secret=self._config['client_secret'],
            user_agent=self._config['user_agent']
        )

        self._image_folder = config.REDDIT_CONFIG["image_folder"]

    def _is_reddit_url(self):
        if 'reddit' in self._url:
            return True
        else:
            self._logger.error('Not an URL Reddit')

    def download_image(self):
        """
        Downloads and saves file(s) harvested from the reddit post
        """
        if self._url is None:
            self._logger.error('No URL found.')

        try:
            reddit_data = requests.get(self._url)

            # Ensure that we're getting response 200
            if reddit_data.status_code != 200:
                self._logger.error(f'Request not completed: {reddit_data}')
                return []

        except requests.exceptions.RequestException as e:
            self._logger.error(f'There was a problem with the request: {e}')
            return []

        # Get the links to which we're going to request
        post = self._reddit_client.submission(url=self._url)
        
        gallery_urls = []

        # Check if the post is multifile or not
        if not hasattr(post, 'media_metadata'):
            gallery_urls.append(post.url)

        else:
            for item in post.media_metadata.items():
                item_url = item[1]['p'][0]['u']
                item_url = item_url.split("?")[0].replace("preview", "i")
                
                gallery_urls.append(item_url)
        
        
        n_of_files = len(gallery_urls)
        self._logger.info(f'About to request {n_of_files} file(s)')
        
        # Request those links and save the content
        for url in gallery_urls:
            
            # First make sure we get the content
            try:
                requested_file = requests.get(url)

                if reddit_data.status_code != 200:
                    self._logger.error(f'Request not completed: {reddit_data}')
                    return []

            except requests.exceptions.RequestException as e:
                self._logger.error(f'There was a problem with the request: {e}')
                return []

            filename = extract_filename(url)
            filepath = os.path.join(self._image_folder, filename)
            
            with open(filepath, 'wb') as f:
                f.write(requested_file.content)
                self._logger.info(f'File saved at {filepath}')
