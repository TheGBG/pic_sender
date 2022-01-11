import os
import requests
from app.utils import extract_filename
from app.logger_client import LoggerClient


class TwitterClient:
    
    def __init__(self, config: dict, logger: LoggerClient):
        """
        Initializes the client for Twitter

        Args:
            config (dict): dictionary containing the keys. Comes from config.
                At the same time, config keys must be set as environment variables
            logger (LoggerClient): instance of the logger
            url (str): link to the tweet
        """
        self._config = config.TWITTER_CONFIG
        self._logger = logger
        
        self._url = None
        self._tweet_id = None

        self._image_folder = self._config['image_folder']
        if not os.path.exists(self._image_folder):
            os.mkdir(self._image_folder)
    
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        self._tweet_id = self._get_tweet_id()

    def _get_tweet_id(self):
        if '/' not in self._url:
            return None
        
        # The id can be found at the end of the url
        return self._url.split('/')[-1].split('?')[0]

    def _get_media_urls(self):
        """
        Builds the link for the API and harvests the content
        """
        if not self._tweet_id:
            return []

        headers = {'Authorization': f'Bearer {self._config["bearer_token"]}'}
        url = f"https://api.twitter.com/2/tweets/{self._tweet_id}?expansions=attachments.media_keys&media.fields=url"

        try:
            tweet_data = requests.get(url=url, headers=headers)
            
            # Ensure that we're getting response 200
            if tweet_data.status_code != 200:
                self._logger.error(f'Request not completed: {tweet_data}')
                return []
        
        except requests.exceptions.RequestException as e:
            self._logger.error(f"There was a problem with the request: {e}")
            return []
        
        media = tweet_data.json().get("includes", {}).get("media", {})
        return [m["url"] for m in media] if media else []

    def download_image(self):
        """
        Downloads and save files(s) harvested from the tweet (images and videos)
        """
        media_urls = self._get_media_urls()
        for url in media_urls:

            # Use the last part of the url as filename. It contains 
            # info about the format
            image_filename = extract_filename(url)

            image_path = os.path.join(self._image_folder, image_filename)
            image_file = requests.get(url)

            with open(image_path, 'wb') as f:
                f.write(image_file.content)

            self._logger.info(f'File saved at {image_path}')
