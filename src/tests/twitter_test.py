from unittest.mock import Mock

import requests
import pytest

from unittest.mock import patch, mock_open
from app.twitter_client import TwitterClient
from config import test_config


class TestTwitterClient:

    def instance_test(self):
        config = test_config
        logger = Mock()
        url = 'fake_url'

        twitter_client = TwitterClient(config, logger, url)

        assert twitter_client._config is config.TWITTER_CONFIG
        assert twitter_client._logger is logger
        assert twitter_client._url is url
        assert twitter_client._tweet_id is None

    def get_tweet_id_ok_test(self):
        config = test_config
        logger = Mock()
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

        twitter_client = TwitterClient(config, logger, url)

        assert twitter_client._tweet_id == '1474892716970442755'

    def get_tweet_id_with_extra_params_ok_test(self):
        config = test_config
        logger = Mock()
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755?more_params_here?123456'

        twitter_client = TwitterClient(config, logger, url)

        assert twitter_client._tweet_id == '1474892716970442755'

    def get_tweet_id_with_wrong_url_test(self):
        config = test_config
        logger = Mock()
        url = 'wrong_url'

        twitter_client = TwitterClient(config, logger, url)

        assert twitter_client._tweet_id is None

    def get_media_urls_ok_test(self):
        config = test_config
        logger = Mock()
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

        twitter_client = TwitterClient(config, logger, url)

        expected_json = {
            'data': 'some data',
            'includes': {
                'media': [
                    {'url': 'fake_url1'},
                    {'url': 'fake_url2'}
                ]
            }
        }
        response = Mock()
        response.json.return_value = expected_json
        response.status_code = 200

        with patch.object(requests, 'get', return_value=response) as mock_get:
            result = twitter_client._get_media_urls()
            
        assert result == ['fake_url1', 'fake_url2']

    def get_media_urls_ko_wrong_url_test(self):
        config = test_config
        logger = Mock()
        url = 'fake_url'

        twitter_client = TwitterClient(config, logger, url)
        response = Mock()

        with patch.object(requests, 'get', return_value=response) as mock_get:
            result = twitter_client._get_media_urls()
            
        assert result == []

    def get_media_urls_ko_request_not_200_test(self):
        config = test_config
        logger = Mock()
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

        twitter_client = TwitterClient(config, logger, url)

        expected_json = {
            'data': 'some data',
            'includes': {
                'media': [
                    {'url': 'fake_url1'},
                    {'url': 'fake_url2'}
                ]
            }
        }
        response = Mock()
        response.json.return_value = expected_json
        response.status_code = 401

        with patch.object(requests, 'get', return_value=response) as mock_get:
            result = twitter_client._get_media_urls()
            
        assert result == []

    def get_media_urls_ko_request_raises_exception_test(self):
        config = test_config
        logger = Mock()
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

        twitter_client = TwitterClient(config, logger, url)

        with patch.object(requests, 'get', side_effect=requests.exceptions.RequestException) as mock_get:
            result = twitter_client._get_media_urls()
            
            assert result == []

    # Not sure about this one because now we dont set the name to save files
    @pytest.mark.skip()
    def download_image_test(self):
        config = test_config
        logger = Mock()
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

        twitter_client = TwitterClient(config, logger, url)
        twitter_client._get_media_urls = Mock(return_value=['url1', 'url2'])

        with patch("builtins.open", mock_open()) as mock_file, patch.object(requests, 'get'):
            twitter_client.download_image()
            mock_file.assert_called_with('images/the_name.jpg', 'wb')
