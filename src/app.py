from PIL.Image import Image
from app.reddit_client import RedditClient
from app.twitter_client import TwitterClient
from app.logger_client import LoggerClient
from app.image_maker import ImageMaker

from config import config


class Container:

    def __init__(self):
        self._logger = LoggerClient(config).get_logger()
        self._logger.info("System starting....")

        self._twitter_url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'
        self._reddit_url = 'https://www.reddit.com/r/ProgrammingJokes/comments/rmulom/whats_on_your_christmas_list/'

        self._twitter_client = TwitterClient(config=config, logger=self._logger)
        self._twitter_client.url = self._twitter_url
        self._reddit_client = RedditClient(config=config, logger=self._logger)
        self._reddit_client.url = self._reddit_url
        self._image_maker = ImageMaker(config=config, logger=self._logger)

    def start(self):
        self._twitter_client.download_image()
        self._reddit_client.download_image('reddit_test')
        self._image_maker.create_image('this', "99")
 

if __name__ == '__main__':
    container = Container()
    container.start()
