import re
from flockbot.helpers.decorators import rate_limited
from flockbot.helpers import EditableContainer
from flockbot.config import Config
from collections import namedtuple
from contextlib import contextmanager
from flockbot.models import Editable
from flockbot.helpers import EditableContainer
import logging


Callback = namedtuple('Callback', ['regex', 'function'])


class Bot:
    def __init__(self, configfile='log/bot.log'):
        self.message_callbacks = {}
        self.comment_callbacks = {}
        self.submission_callbacks = {}

        self.config = Config()
        self.config.set_logging(configfile)
        self.reply_text = ''
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def database(self):
        session = self.config.database
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def login(self, useragent, oauth_info, refresh_token):
        self.reddit = praw.Reddit(useragent=useragent)
        self.config.set_oauth_info(self.reddit, oauth_info, refresh_token)

    def check_messages(self, mark_read=False):
        """ Get the users unread messages
            and check for callback triggers.

            Args:
                mark_read: (bool) if True, mark the messages as read

            Returns:
                Number of messages read.
        """
        if len(self.message_callbacks) == 0:
            return
        messages = self.reddit.get_unread(unset_has_mail=mark_read)
        total_read = 0
        for message in messages:
            with self.database() as db:
                editable = Editable(message)
                if db.query(Editable).filter(Editable.id == editable.id):
                    if mark_read:
                        message.mark_as_read()
                    continue

                # if a callback was made, mark as read.
                if self.check_callbacks(editable, self.message_callbacks) or mark_read:
                    message.mark_as_read()
                    total_read += 1
                db.add(Editable(id=editable.id))
        return total_read

    def check_comments(self, subreddit):
        """ Check the latest comments for callbacks """
        if len(self.comment_callbacks) == 0:
            return
        last_comment = self.last_visited.get(subreddit, None)
        comments = self.reddit.get_comments(
            subreddit=subreddit,
            place_holder=last_comment,
            limit=25
        )
        for comment in comments:
            with self.database() as db:
                editable = EditableContainer(comment)
                if db.query(Editable).filter(Editable.id==editable.id):
                    continue

                self.check_callbacks(editable, self.comment_callbacks)

                db.add(Editable(id=editable.id))

    def check_submissions(self, subreddit):
        """ Check the latest submissions for callbacks """
        if len(self.submission_callbacks) == 0:
            return
        last_submission = self.last_visited_submission.get(subreddit, None)
        submissions = self.reddit.get_subreddit(subreddit).get_new(
            place_holder=last_submission,
            limit=25
        )
        for submission in submissions:
            with self.database() as db:
                editable = EditableContainer(submission)
                if db.query(Editable).filter(Editable.id==editable.id):
                    continue
                self.check_callbacks(editable, self.submission_callbacks)
                db.add(Editable(id=editable.id))

    def check_callbacks(self, editable, callbacks):
        """ Iterates over registered callbacks

            If the editable contains text that triggers a registered callback,
            it calls that functions with the editable and matched text
            as the arguments.

            Args:
                editable: (helper.Editable) the editable to check for triggers
                callbacks: dictionary of callbacks. Key: regex, value: function
            Returns:
                True, when a callback was triggered
                False, otherwise
        """
        has_callback = False
        for regex, functions in callbacks.items():
            string = editable.text
            match = re.findall(regex, string, re.IGNORECASE)
            if match:
                has_callback = True
                for callback_function in functions:
                    reply = callback_function(editable, match)
                    if isinstance(reply, str):
                        self.build_reply(reply)
        if has_callback:
            self.reply_to(editable)
        return has_callback

    def _register_callback(self, container, callback):
        """ Register a callback in the specified dictionary 

            Args:
                container: dictionary containing regex as keys, functions as values
                callback: namedtuple containing a regex and a function attribute
        """
        container.setdefault(callback.regex, [])\
                 .append(callback.function)

    def register_message_callback(self, callback):
        self._register_callback(self.message_callbacks, callback)

    def register_comment_callback(self, callback):
        self._register_callback(self.comment_callbacks, callback)

    def register_submission_callback(self, callback):
        self._register_callback(self.submission_callbacks, callback)

    def build_reply(self, text):
        """ Creates a new reply or appends to an existing one. """
        if not text:
            return
        if not self.reply_text:
            self.reply_text = text
        else:
            self.reply_text += text
        # Add spacer
        self.reply_text += '\n___\n'

    @rate_limited
    def reply_to(self, editable, text=None):
        """ Comments on the object

            Args:
                editable: (helper.Editable) the editable to reply to
                text: (string) markdown message to put in the comment
        """
        self.build_reply(text)
        if not self.reply_text:
            return
        self.reply_text += self.config.footer
        self.logger.debug('Reply {id}: {msg}'.format(
            id=editable.id, msg=self.reply_text)
        )
        editable.reply(self.reply_text)

        # reset reply text
        self.reply_text = ''