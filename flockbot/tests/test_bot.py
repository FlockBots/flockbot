import unittest
from flockbot import Bot
from flockbot.bot import Callback

class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = Bot()

    def tearDown(self):
        pass

    def test_callbackRegistration(self):
        subRegex = 'sub_regex'
        msgRegex = 'msg_regex'
        cmtRegex = 'cmt_regex'
        subCallback = Callback(regex=subRegex, function=lambda: 'sub')
        msgCallback = Callback(regex=msgRegex, function=lambda: 'msg')
        cmtCallback = Callback(regex=cmtRegex, function=lambda: 'cmt')
        self.bot.register_submission_callback(subCallback)
        self.bot.register_message_callback(msgCallback)
        self.bot.register_comment_callback(cmtCallback)

        self.assertEqual(self.bot.submission_callbacks[subRegex][0](), 'sub')
        self.assertEqual(self.bot.message_callbacks[msgRegex][0](), 'msg')
        self.assertEqual(self.bot.comment_callbacks[cmtRegex][0](), 'cmt')