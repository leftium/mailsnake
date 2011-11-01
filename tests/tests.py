#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from test_settings import MAILCHIMP_API_KEY, MAILCHIMP_LIST_ID
from mailsnake import MailSnake
ms = MailSnake(MAILCHIMP_API_KEY)

class MailSnakeTestSuite(unittest.TestCase):
    def test_listSubscribe(self):
        response = ms.listSubscribe(id=MAILCHIMP_LIST_ID, email_address="test@testss.es", double_optin=False)
        self.assertTrue(response)

if __name__ == '__main__':
    unittest.main()
