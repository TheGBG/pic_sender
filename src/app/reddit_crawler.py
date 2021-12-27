import praw
import os
import requests
from app.utils import get_random_string


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
