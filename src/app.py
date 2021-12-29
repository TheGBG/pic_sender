from app.reddit_client import RedditClient
from app.twitter_client import TwitterClient
from app.logger_client import LoggerClient

from config import config


class Container:

    def __init__(self):
        self._logger = LoggerClient(config).get_logger()
        self._logger.info("System starting....")

        self._twitter_url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'
        self._reddit_url = 'https://www.reddit.com/r/ProgrammingJokes/comments/rmulom/whats_on_your_christmas_list/'

        self._twitter_client = TwitterClient(config=config, logger=self._logger, url=self._twitter_url)
        self._reddit_client = RedditClient(config=config, logger=self._logger, url=self._reddit_url)

    def start(self):
        self._twitter_client.download_image(image_name='testing_twitter_name')
        self._twitter_client.download_image()

        self._reddit_client.download_image(image_name='testing_reddit_name')
        self._reddit_client.download_image()


if __name__ == '__main__':
    container = Container()
    container.start()
