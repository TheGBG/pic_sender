import random
import string

def get_random_string():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))