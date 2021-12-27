from unittest.mock import Mock

import requests
from unittest.mock import patch, mock_open
from app.twitter_crawler import TwitterCrawler
from config import test_config


class TestTwitterCrawler:

    def instance_test(self):
        config = test_config.TWITTER_CONFIG
        url = 'fake_url'

        twitter_crawler = TwitterCrawler(config, url)

        assert twitter_crawler._config is config
        assert twitter_crawler._url is url
        assert twitter_crawler._tweet_id is None

    def get_tweet_id_ok_test(self):
        config = test_config.TWITTER_CONFIG
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

        twitter_crawler = TwitterCrawler(config, url)

        assert twitter_crawler._tweet_id == '1474892716970442755'

    def get_tweet_id_with_extra_params_ok_test(self):
        config = test_config.TWITTER_CONFIG
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755?more_params_here?123456'

        twitter_crawler = TwitterCrawler(config, url)

        assert twitter_crawler._tweet_id == '1474892716970442755'

    def get_tweet_id_with_wrong_url_test(self):
        config = test_config.TWITTER_CONFIG
        url = 'wrong_url'

        twitter_crawler = TwitterCrawler(config, url)

        assert twitter_crawler._tweet_id is None

    def get_media_urls_ok_test(self):
        config = test_config.TWITTER_CONFIG
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

        twitter_crawler = TwitterCrawler(config, url)

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
            result = twitter_crawler._get_media_urls()
            
            assert result == ['fake_url1', 'fake_url2']

    def get_media_urls_ko_wrong_url_test(self):
        config = test_config.TWITTER_CONFIG
        url = 'fake_url'

        twitter_crawler = TwitterCrawler(config, url)
        response = Mock()

        with patch.object(requests, 'get', return_value=response) as mock_get:
            result = twitter_crawler._get_media_urls()
            
            assert result == []

        #with pytest.raises(HTTPError):
        #    resp = get_employee(test_id)

    def get_media_urls_ko_request_not_200_test(self):
        config = test_config.TWITTER_CONFIG
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

        twitter_crawler = TwitterCrawler(config, url)

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
            result = twitter_crawler._get_media_urls()
            
            assert result == []

    def get_media_urls_ko_request_raises_exception_test(self):
        config = test_config.TWITTER_CONFIG
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

        twitter_crawler = TwitterCrawler(config, url)

        with patch.object(requests, 'get', side_effect=requests.exceptions.RequestException) as mock_get:
            result = twitter_crawler._get_media_urls()
            
            assert result == []

    def download_image_test(self):
        config = test_config.TWITTER_CONFIG
        url = 'https://twitter.com/nocontextroyco/status/1474892716970442755'

        twitter_crawler = TwitterCrawler(config, url)
        twitter_crawler._get_media_urls = Mock(return_value=['url1', 'url2'])

        with patch("builtins.open", mock_open()) as mock_file, patch.object(requests, 'get'):
                twitter_crawler.download_image(image_name='the_name')
                mock_file.assert_called_with('images/the_name.jpg', 'wb')
