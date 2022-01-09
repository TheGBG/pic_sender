from unittest.mock import Mock
import prawcore

import requests
import praw
import pytest
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

    def download_image_ko_status_code_not_200_test(self):
        config = test_config
        logger = Mock()
        url_no_image = 'https://www.reddit.com/user/ElonBrust/comments/rrhac2/invalid_url/'
        
        reddit_client = RedditClient(config, logger, url_no_image)

        expected_response = requests.Response()
        expected_response.status_code = 400

        with patch.object(
            requests,
            'get',
            return_value=expected_response
            ) as mock_get:
            
            result = reddit_client.download_image()
            
            assert result == []

    # Not sure about this two tests now
    @pytest.mark.skip()
    def download_image_ko_no_image_in_post_test(self):
        config = test_config
        logger = Mock()
        url_no_image = 'https://www.reddit.com/user/ElonBrust/comments/rrhac2/fake_post_with_no_image/'
        
        reddit_client = RedditClient(config, logger, url_no_image)

        expected_response = requests.Response()
        expected_response.status_code = 200

        # Aquí tienes que patchear tanto get como el submission
        with patch.object(
            requests,
            'get',
            return_value=expected_response
            ) as mock_get, patch.object(
            praw.Reddit,
            'submission',
            ) as mock_sub:
            
            # Y aquí pseudo-patcheamos el .url xd
            mock_sub.return_value.url = 'some_image_url_with_no_._j_p_g'
            result = reddit_client.download_image()

            assert result == []
    
    @pytest.mark.skip()
    def download_image_ok_test(self):
        config = test_config
        logger = Mock()
        url_no_image = 'https://www.reddit.com/user/ElonBrust/comments/rrhac2/fake_post_with_no_image/'
        
        reddit_client = RedditClient(config, logger, url_no_image)

        expected_response = requests.Response()
        expected_response.status_code = 200

        # Aquí tienes que patchear tanto get como submission como open (se va complicando)
        with patch.object(
            requests,
            'get',
            return_value=expected_response
            ) as mock_get, patch.object(
            praw.Reddit,
            'submission',
            ) as mock_sub, patch(
            "builtins.open", 
            mock_open()
            ) as mock_file:
            
            # Y aquí pseudo-patcheamos el .url
            mock_sub.return_value.url = 'some_image_url_with.jpg'
            result = reddit_client.download_image()

            #mock_file.assert_called_with('images/the_name.jpg', 'wb')