# pic_sender

How should we start?

1. We need a way to download an image, given a
link. This link can be either Reddit or Twitter
2. Create a Telegram bot that uses that code to
download the image, and then send it to a chat
3. Add the bot to the TG group

To clone this repo, run
```
git clone https://github.com/gabrielblancogarcia/pic_sender.git
``` 


To install the required libraries, run
```
pip install -r requirements.txt
```

Quick twitter test:
```
twitter_url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

twitter = TwitterClient(
    config=test_config.TWITTER_CONFIG
    url=twitter_url,

)

twitter.download_image(image_name='testing_twitter_name')
twitter.download_image()
```

Quick reddit test:
```
reddit = RedditClient(
    client_id=test_config.REDDIT_CONFIG['client_id'],
    client_secret=test_config.REDDIT_CONFIG['client_secret'],
    user_agent=test_config.REDDIT_CONFIG['user_agent']
)

example_url = 'https://www.reddit.com/r/ProgrammingJokes/comments/rmulom/whats_on_your_christmas_list/'
reddit.set_post_url(example_url)

reddit.download_image(image_name='testing_reddit_name')
reddit.download_image()


# TODO: what happens if the post has more than 1 image?
multi_images = 'https://www.reddit.com/user/ElonBrust/comments/rnjqqk/testing_this/'
```


To run the tests:
```
cd pic_sender
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
pytest --cov
```