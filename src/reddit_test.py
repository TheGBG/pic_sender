from crawlers import RedditCrawler
from config.config import REDDIT_CONFIG

reddit = RedditCrawler(
    client_id=REDDIT_CONFIG['client_id'],
    client_secret=REDDIT_CONFIG['client_secret'],
    user_agent=REDDIT_CONFIG['user_agent']
)

example_url = 'https://www.reddit.com/r/ProgrammingJokes/comments/rmulom/whats_on_your_christmas_list/'
reddit.set_post_url(example_url)

reddit.download_image(image_name='testing_reddit_name')
reddit.download_image()


# TODO: what happens if the post has more than 1 image?
multi_images = 'https://www.reddit.com/user/ElonBrust/comments/rnjqqk/testing_this/'