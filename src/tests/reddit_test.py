from unittest.mock import Mock
import prawcore

import requests
import praw
from unittest.mock import patch, mock_open
from app.reddit_client import RedditClient
from config import test_config


class TestRedditClient:
    
    def instance_test(self):
        config = test_config
        logger = Mock()
        url = 'fake_url'

        reddit_client = RedditClient(config, logger, url)

        assert reddit_client._config is config.REDDIT_CONFIG
        assert reddit_client._logger is logger
        assert reddit_client._url is url

    def is_reddit_url_ok_test(self):
        config = test_config
        logger = Mock()
        url = 'reddit/fake_post'

        reddit_client = RedditClient(config, logger, url)
        result = reddit_client._is_reddit_url()
        
        assert result is True

    def is_reddit_url_ko_test(self):
        config = test_config
        logger = Mock()
        url = 'facebook/fake_post'

        reddit_client = RedditClient(config, logger, url)
        result = reddit_client._is_reddit_url()

        assert result is not True

    def download_image_ko_request_raises_exception_test(self):
        config = test_config
        logger = Mock()
        url = 'https://www.reddit.com/user/ElonBrust/comments/rrggot/fake_post_to_delete/'
        
        reddit_client = RedditClient(config, logger, url)

        with patch.object(
            requests,
            'get',
            side_effect=requests.exceptions.RequestException
            ) as mock_get:
            
            result = reddit_client.download_image()
            
            assert result == []

    def download_image_ko_no_image_in_post(self):
        config = test_config
        logger = Mock()
        url_no_image = 'https://www.reddit.com/user/ElonBrust/comments/rrhac2/fake_post_with_no_image/'
        
        reddit_client = RedditClient(config, logger, url_no_image)

        with patch.object(
            praw.Reddit,
            'submmit',
            side_effect=prawcore.exceptions.ResponseException
            ) as mock_get:
            
            result = reddit_client.download_image()
            
            assert result == []

    def download_image_ok_no_image_in_post(self):
        config = test_config
        logger = Mock()
        url = 'https://www.reddit.com/r/MechanicalKeyboards/comments/rra1u9/first_custom_mechanical_keyboard_tofu60_dz60/'

        reddit_client = RedditClient(config, logger, url)

        with patch.object(
            requests,
            'get',
            side_effect=requests.exceptions.RequestException
            ) as mock_get:
            
            result = reddit_client.download_image()
            
            assert result != []

