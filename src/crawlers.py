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

        with open(image_path, 'wb') as f:
            f.write(requested_image.content)
        
        print(f'Iamge saved at {image_path}')
