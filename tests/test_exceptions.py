from mailsnake import MailSnake, exceptions

from .config import (
    MAILCHIMP_API_KEY, MAILCHIMP_LIST_ID, TEST_RECIPIENT_EMAIL,
    MANDRILL_API_KEY
)

import unittest


class MailSnakeExceptionsTestCase(unittest.TestCase):
    def setUp(self):
        self.mcapi = MailSnake(MAILCHIMP_API_KEY)
        self.bad_mcapi = MailSnake('WRONGKEY-us1')

    def test_invalid_apikey_exception(self):
        """Test passing the wrong API Key will raise an InvalidApiKeyException"""
        self.assertRaises(exceptions.InvalidApiKeyException, self.bad_mcapi.lists)
