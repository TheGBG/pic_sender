from crawlers import RedditCrawler
from config import config

reddit = RedditCrawler(
    client_id='ThuWk73bhi78WFOZ2hOY1A',
    client_secret='a0tBZ_RBH2eq5U4KDpLKFl7GrKe3Fg',
    user_agent='elonbrust'
)

example_url = 'https://www.reddit.com/r/ProgrammingJokes/comments/rmulom/whats_on_your_christmas_list/'
reddit.set_post_url(example_url)

reddit.download_image()


# TODO: what happens if the post has more than 1 image?
multi_images = 'https://www.reddit.com/user/ElonBrust/comments/rnjqqk/testing_this/'