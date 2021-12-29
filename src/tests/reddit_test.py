from unittest.mock import Mock

import requests
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

    def get_download_image_ko_request_raises_exception_test(self):
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



    def download_image_ok_test(self):
        pass

    def download_image_ko_request_not_200(self):    
        pass

    def download_image_ko_url_not_provided(self):
        pass

