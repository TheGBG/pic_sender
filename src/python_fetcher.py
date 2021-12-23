import requests
import random
import string
from config import config


def get_media_urls(tweet_id):
    if not tweet_id:
        return []

    headers = {'Authorization': f'Bearer {config.TWITTER_CONFIG["bearer_token"]}'}
    url = f"https://api.twitter.com/2/tweets/{tweet_id}?expansions=attachments.media_keys&media.fields=url"

    try:
        r = requests.get(url=url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(f"There was a problem with the request: {e}")
        return []

    media = r.json().get("includes", {}).get("media", {})
    return [m["url"] for m in media] if media else []

def get_images(urls):
    for u in urls:
        with open(f'images/{get_random_string()}.jpg', 'wb') as f:
            f.write(requests.get(u).content)

def get_random_string():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))

def get_tweet_id_from_url(url):
    if '/' not in url:
        return None

    return url.split('/')[-1].split('?')[0]

url = "https://twitter.com/archillect/status/1474142933842632706"
id = get_tweet_id_from_url(url)
media_urls = get_media_urls(id)
get_images(media_urls)

# TODO: Delete images
