from crawlers import TwitterCrawler
from config.config import TWITTER_CONFIG

twitter_url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

twitter = TwitterCrawler(
    post_url=twitter_url,
    twitter_config=TWITTER_CONFIG
)

twitter.download_image(image_name='testing_twitter_name')
twitter.download_image()