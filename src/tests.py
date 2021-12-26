from crawlers import RedditCrawler
from crawlers import TwitterCrawler
from config import config

# ============================== Twitter example =============================
twitter_url = "https://twitter.com/archillect/status/1474142933842632706"

twitter = TwitterCrawler(
    post_url=twitter_url,
    twitter_config=config.TWITTER_CONFIG
)

twitter.download_image()


# =============================== Reddit example ============================= 
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