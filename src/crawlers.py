import praw
import os
import requests
from utils import get_random_string

class RedditCrawler(praw.Reddit):
    
    # init constructor will be the one from parent class
    def set_post_url(self, post_url):
        self.post_url = post_url
    
    def download_image(self, image_folder='images', image_format='.jpg'):
        
        if self.post_url is None:
            print('Please, set an url with set_post_url()')
        
        # Use parent subbmission method
        post = super().submission(url=self.post_url)
        image_url = post.url
        
        image_name = f'{get_random_string()}{image_format}'
        image_path = os.path.join(image_folder, image_name)
        
        requested_image = requests.get(image_url)
        # Ensure that we're getting response 200
        if not requested_image.ok:
            print(f'Request not completed: {requested_image}')

        with open(image_path, 'wb') as f:
            f.write(requested_image.content)
            f.close()
        
        print(f'Image saved at {image_path}')

class TwitterCrawler:
    
    def __init__(self, post_url, twitter_config):
        self.post_url = post_url
        self.twitter_config = twitter_config
        self._get_tweet_id()
    
    def _get_tweet_id(self):
        if '/' not in self.post_url:
            return None
            
        tweet_id = self.post_url.split('/')[-1].split('?')[0]
        self.tweet_id = tweet_id

    def _get_media_urls(self):
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

    def download_image(self, image_folder='images', image_format='.jpg'):
        media_urls = self._get_media_urls()
        for url in media_urls:
            
            # Gather elements for image saving, save and print feedback
            image_name = f'{get_random_string()}{image_format}'
            image_path = os.path.join(image_folder, image_name)
            image_file = requests.get(url)

            with open(image_path, 'wb') as f:
                f.write(image_file.content)
                f.close()

            print(f'Image saved at {image_path}')
