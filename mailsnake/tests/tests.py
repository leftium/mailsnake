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

    def test_templates(self):
        types = {'user': False, 'gallery': False, 'base': False}
        for t_type in types:
            new_types = dict(types.items() + {t_type: True}.items())
            assert self.mcapi.templates(types=new_types).has_key(t_type)

    def test_templateAddDel(self):
        templates = self.mcapi.templates(inactives={'include': True})
        template_names = [t['name'] for t in templates['user']]
        html = open('mailsnake/tests/template.html', 'r').read()
        index = 0
        base_name = 'mailsnake_test_template'
        template_name = '%s%i' % (base_name, index)
        while template_name in template_names:
            index += 1
            template_name = '%s%i' % (base_name, index)
        template_id = self.mcapi.templateAdd(name=template_name, html=html)
        assert isinstance(template_id, int)
        assert self.mcapi.templateDel(id=template_id)
