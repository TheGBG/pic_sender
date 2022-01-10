import random
import string

def get_random_string():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))

def extract_filename(url: str, separator: str = '/'):
    return url.split(separator)[-1]