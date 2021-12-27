import praw
import os
import requests
from utils import get_random_string

class RedditCrawler(praw.Reddit):
    
    # init constructor will be the one from parent class
    def set_post_url(self, post_url:str):
        """
        Sets the url of the Reddit post to scrap.

        Arguments
        ---------
            - post_url (str): link to the post. Can be either the URL bar
              link or the "share" button link. 
        """
        self.post_url = post_url
    
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
        if self.post_url is None:
            print('Please, set an url with set_post_url()')
        
        # Use parent subbmission method
        post = super().submission(url=self.post_url)
        image_url = post.url        
        requested_image = requests.get(image_url)
        
        # Ensure that we're getting response 200
        if not requested_image.ok:
            print(f'Request not completed: {requested_image}')

        if image_name is None:
            image_name = get_random_string()

        image_filename = f'{image_name}{image_format}' 
        image_path = os.path.join(image_folder, image_filename)
        
        with open(image_path, 'wb') as f:
            f.write(requested_image.content)
            f.close()
        
        print(f'Image saved at {image_path}')

class TwitterCrawler:
    
    def __init__(self, post_url: str, twitter_config: dict):
        """
        Initializes the crawler for Twitter

        Args:
            post_url (str): link to the tweet
            twitter_config (dict): dictionary containing the keys. Comes from
            config. At the same time, config keys must be set as environment
            variables
        """
        self.post_url = post_url
        self.twitter_config = twitter_config
        self._get_tweet_id()
    
    def _get_tweet_id(self):
        if '/' not in self.post_url:
            return None
        
        # The id can be fond at the end of the url
        tweet_id = self.post_url.split('/')[-1].split('?')[0]
        self.tweet_id = tweet_id

    def _get_media_urls(self):
        """
        Builds the link for the API and harvests the content
        """
        if not self.tweet_id:
            return []

        headers = {'Authorization': f'Bearer {self.twitter_config["bearer_token"]}'}
        url = f"https://api.twitter.com/2/tweets/{self.tweet_id}?expansions=attachments.media_keys&media.fields=url"

        try:
            requested_image = requests.get(url=url, headers=headers)
            
            # Ensure that we're getting response 200
            if not requested_image.ok:
                print(f'Request not completed: {requested_image}')
        
        except requests.exceptions.RequestException as e:
            print(f"There was a problem with the request: {e}")
            return []
        
        media = requested_image.json().get("includes", {}).get("media", {})
        return [m["url"] for m in media] if media else []

    def download_image(
        self,
        image_name: str = None,
        image_folder: str = 'images',
        image_format: str = '.jpg'
    ):
        """
        Downloads and save image(s) harvested from the tweet

        Arguments
        ---------
            - image_name: (str, optional): name for the image. When `None`, a
              random string will be set as name.

            - image_folder (str, optional): where to store the images.
              Defaults to 'images'.

            - image_format (str, optional): defaults to '.jpg'.
        """
        media_urls = self._get_media_urls()
        for url in media_urls:
            
            # Gather elements for image saving, save and print feedback
            if image_name is None:
                image_name = get_random_string()
            
            image_filename = f'{image_name}{image_format}'
            image_path = os.path.join(image_folder, image_filename)
            image_file = requests.get(url)

            with open(image_path, 'wb') as f:
                f.write(image_file.content)
                f.close()

            print(f'Image saved at {image_path}')
