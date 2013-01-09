import unittest

from collections import MutableSequence
from mailsnake import MailSnake
from random import random

from .secret_keys import MAILCHIMP_API_KEY, MAILCHIMP_LIST_ID, TEST_EMAIL

"""
To run these tests, do the following:
- Place a file called secret_keys.py under the mailsnake directory
  containing the following mailchimp keys:
  * MAILCHIMP_API_KEY
  * MAILCHIMP_LIST_ID
  You must create a test list in MailChimp and get the ID for use here
  because the API does not have a method for creating lists.

- Install the python 'nose' library
- From the command-line, run 'nosetests'
"""


class TestMailChimpAPI(unittest.TestCase):
    def setUp(self):
        self.mcapi = MailSnake(MAILCHIMP_API_KEY)

    # Helper Methods

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

    # Campaign Related Methods

    def test_campaignCreateDelete(self):
        template_id = self._add_test_template()
        from_email = self.mcapi.getAccountDetails()['contact']['email']
        options = {
            'list_id': MAILCHIMP_LIST_ID, 'subject': 'testing',
            'from_email': from_email, 'from_name': 'Test From',
            'to_name': 'Test To', 'template_id': template_id,
            'inline_css': True, 'generate_text': True, 'title': 'testing'
        }
        test_content = '%f' % random()
        content = {'html_std_content00': test_content}
        campaign_id = self.mcapi.campaignCreate(
            type='regular', options=options, content=content)
        assert isinstance(campaign_id, unicode)
        campaign_content = self.mcapi.campaignContent(cid=campaign_id)
        assert 'html' in campaign_content
        assert 'text' in campaign_content
        assert test_content in campaign_content['html']
        assert test_content in campaign_content['text']
        default_content = 'default content'
        assert not default_content in campaign_content['html']
        assert not default_content in campaign_content['text']

        # Clean up
        assert self.mcapi.campaignDelete(cid=campaign_id)
        assert self.mcapi.templateDel(id=template_id)

    # List Related Methods

    def test_lists(self):
        lists = self.mcapi.lists()
        assert isinstance(lists, dict)
        assert 'total' in lists
        assert 'data' in lists

    def test_listActivity(self):
        activity = self.mcapi.listActivity(id=MAILCHIMP_LIST_ID)
        assert isinstance(activity, list)

    def test_listSubscribeUnsubscribe(self):
        assert self.mcapi.listSubscribe(
            id=MAILCHIMP_LIST_ID, email_address=TEST_EMAIL, double_optin=False,
            send_welcome=False)
        assert self.mcapi.listUnsubscribe(
            id=MAILCHIMP_LIST_ID, email_address=TEST_EMAIL, send_goodbye=False,
            send_notify=False)

    # Template Related Methods

    def test_templates(self):
        types = {'user': False, 'gallery': False, 'base': False}
        for t_type in types:
            new_types = dict(types.items() + {t_type: True}.items())
            assert t_type in self.mcapi.templates(types=new_types)

    def test_templateAddDel(self):
        template_id = self._add_test_template()
        assert isinstance(template_id, int)
        assert self.mcapi.templateDel(id=template_id)

    def _add_test_template(self):
        html = open('mailsnake/tests/template.html', 'r').read()
        templates = self.mcapi.templates(inactives={'include': True})
        template_names = [t['name'] for t in templates['user']]
        index = 0
        base_name = 'mailsnake_test_template'
        template_name = '%s%i' % (base_name, index)
        while template_name in template_names:
            index += 1
            template_name = '%s%i' % (base_name, index)
        return self.mcapi.templateAdd(name=template_name, html=html)
