from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import praw
import logging

class Config:
    
    def __init__(self):
        self.complete = {
            'oauth': False,
            'database': False,
            'logging': False,
            'subscriptions': False
        }

    def set_oauth_info(self, reddit, oauth_info, refresh_token):        
        reddit.set_oauth_app_info(oauth_info)
        reddit.refresh_access_information(refresh_token)
        self.complete['oauth'] = True

    @property
    def database(self):
        """ Create a new sessions """
        return self._database()

    @database.setter
    def database(self, filename):
        """ Create a sessionmaker """
        database_engine = create_engine('sqlite:///' + filename, echo=False)
        self._database = sessionmaker(bind=database_engine)
        self.complete['database'] = True


    def set_logging(self, logfile, level=logging.INFO):
        logging.basicConfig(
            filename=logfile,
            level=level,
            format='{asctime:<19.19} | {name:<20.20} | {levelname:<6.6} | {message}',
            style='{'
        )
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler())
        # requests_logger = logging.getLogger('requests')
        # requests_logger.setLevel(logging.WARNING)
        self.complete['logging'] = True
        return logger

    def set_reply_footer(self, footer):
        self.footer = footer

    def set_subscriptions(self, subreddits):
        self.subreddits = subreddits
        self.complete['subscriptions'] = True
