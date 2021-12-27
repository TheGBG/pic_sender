from crawlers import TwitterCrawler
from config import config

twitter_url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

twitter = TwitterCrawler(
    post_url=twitter_url,
    twitter_config=config.TWITTER_CONFIG
)

twitter.download_image()