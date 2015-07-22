import unittest
from flockbot import Bot
from flockbot.bot import Callback

class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = Bot()

    def tearDown(self):
        pass

    def test_callbackFunctionRegistration(self):
        subRegex = 'sub_regex'
        msgRegex = 'msg_regex'
        cmtRegex = 'cmt_regex'
        subCallback = function=lambda: 'sub'
        msgCallback = function=lambda: 'msg'
        cmtCallback = function=lambda: 'cmt'
        self.bot.register_callback('submission', subRegex, subCallback)
        self.bot.register_callback('message', msgRegex, msgCallback)
        self.bot.register_callback('comment', cmtRegex, cmtCallback)

        self.assertEqual(self.bot.submission_callbacks[subRegex][0](), 'sub')
        self.assertEqual(self.bot.message_callbacks[msgRegex][0](), 'msg')
        self.assertEqual(self.bot.comment_callbacks[cmtRegex][0](), 'cmt')

    def test_callbackControllerRegistration(self):
        pass