import unittest

from collections import MutableSequence
from mailsnake import MailSnake
from .secret_keys import MAILCHIMP_API_KEY

class TestMailChimpAPI(unittest.TestCase):
    def setUp(self):
        self.mcapi = MailSnake(MAILCHIMP_API_KEY)

    def test_ping(self):
        assert self.mcapi.ping() == "Everything's Chimpy!"

    def test_chimpChatter(self):
        chimp_chatter = self.mcapi.chimpChatter()
        # Check that the result is a list
        assert isinstance(chimp_chatter, MutableSequence)
        # If the list is not empty, check a few keys
        if len(chimp_chatter) > 0:
            assert 'message' in chimp_chatter[0].keys()
            assert chimp_chatter[0]['url'].find('mailchimp') > -1
