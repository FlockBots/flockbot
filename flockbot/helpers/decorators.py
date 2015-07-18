import praw
import logging
import time

def rate_limited(function):
    """ Tries to execute a Reddit API related function. 
        If the Reddit rate limit is exceeded, it sleeps for a sufficient amount of time before retrying.
    """
    def wrapper(*args, **kwargs):
        while True:
            try:
                result = function(*args, **kwargs)
                break
            except praw.errors.RateLimitExceeded as error:
                logging.warning('RateLimitExceeded | Sleeping {0} seconds'.format(error.sleep_time))
                time.sleep(error.sleep_time)
        return result
    return wrapper