import praw
import logging
import time

def rate_limited(function):
    """ Tries to execute a Reddit API related function. 
        If the Reddit rate limit is exceeded, it sleeps
        for a sufficient amount of time before retrying.
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

def callback(editable, regex):
    """ Adds the regex to the _callback attribute of the function """
    def decorator(function):
        if not hasattr(function, '_callbacks'):
            function._callbacks = {}
        function._callbacks.setdefault(editable, [])\
            .append(regex)
        return function
    return decorator

