# -*- coding: utf-8 -*-

"""
mailsnake.api
~~~~~~~~~~~~~

This module contains functionality for access to core Twitter API calls,
Twitter Authentication, and miscellaneous methods that are useful when
dealing with the Twitter API
"""


import requests
from .compat import json, basestring

from . import __version__
from .exceptions import *

import collections
import types


class MailSnake(object):
    def __init__(self, apikey='', extra_params=None, api='api', api_section='',
                 requests_opts=None, dc=None):
        """Cache API key and address. For additional control over how
        requests are made, supply a dictionary for requests_opts. This will
        be passed through to requests.post() as kwargs.
        """

        ACCEPTED_APIS = ('api', 'sts', 'export', 'mandrill')
        if not api in ACCEPTED_APIS:
            raise MailSnakeException('The API "%s" is not supported.') % api

        self.api = api
        self.apikey = apikey
        self.dc = self.apikey.split('-')[1] if '-' in self.apikey else dc

        self.default_params = {'apikey': apikey}
        extra_params = extra_params or {}
        if api == 'mandrill':
            self.default_params = {'key': apikey}
            if api_section != '':
                self.api_section = api_section
            else:
                # Mandrill divides the api into different sections
                for x in ['users', 'messages', 'tags', 'rejects',
                          'senders', 'urls', 'templates', 'webhooks']:
                    setattr(self, x, MailSnake(apikey, extra_params,
                                               api, x))
        self.default_params.update(extra_params)

        api_info = {
            'api': (self.dc, '.api.', 'mailchimp', '1.3/?method='),
            'sts': (self.dc, '.sts.', 'mailchimp', '1.0/'),
            'export': (self.dc, '.api.', 'mailchimp', 'export/1.0/'),
            'mandrill': ('', '', 'mandrillapp', 'api/1.0/'),
        }
        self.api_url = 'https://%s%s%s.com/%s' % api_info[api]

        self.requests_opts = requests_opts or {}
        default_headers = {'User-Agent': 'MailSnake v' + __version__}
        if not 'headers' in self.requests_opts:
            # If they didn't set any headers, set our defaults for them
            self.requests_opts['headers'] = default_headers
        elif 'User-Agent' not in self.requests_opts['headers']:
            # If they set headers, but didn't include User-Agent.. set it for them
            self.requests_opts['headers'].update(default_headers)

        if self.api == 'api' or self.api == 'mandrill':
            self.requests_opts['headers'].update({'content-type': 'application/json'})
        else:
            self.requests_opts['headers'].update({'content-type': 'application/x-www-form-urlencoded'})

        self.client = requests.Session()
        # Make a copy of the client args and iterate over them
        # Pop out all the acceptable args at this point because they will
        # Never be used again.
        requests_opts_copy = self.requests_opts.copy()
        for k, v in requests_opts_copy.items():
            if k in ('cert', 'headers', 'hooks', 'max_redirects', 'proxies'):
                setattr(self.client, k, v)
                self.requests_opts.pop(k)  # Pop, pop!

    def __repr__(self):
        if self.api == 'api':
            api = 'API v3'
        elif self.api == 'sts':
            api = self.api.upper() + ' API'
        else:
            api = self.api.capitalize() + ' API'

        return '<MailSnake %s: %s>' % (api, self.apikey)

    def call(self, method, params=None):
        """Call the appropriate MailChimp API method with supplied
        params. If response streaming is enabled, return a generator
        that yields one line of deserialized JSON at a time, otherwise
        simply deserialize and return the entire JSON response body.
        """
        url = self.api_url
        if self.api == 'mandrill':
            url += (self.api_section + '/' + method + '.json')
        elif self.api == 'sts':
            url += (method + '.json/')
        else:
            url += method

        params = params or {}
        params.update(self.default_params)

        if self.api == 'api' or self.api == 'mandrill':
            data = json.dumps(params)
            if self.api == 'api':
                data = requests.utils.quote(data)
        elif self.api == 'export':
            data = flatten_data(params)
        else:
            data = params

        try:
            requests_args = {}
            for k, v in self.requests_opts.items():
                # Maybe this should be set as a class variable and only done once?
                if k in ('timeout', 'allow_redirects', 'stream', 'verify'):
                    requests_args[k] = v

            req = self.client.post(url, data=data, **requests_args)
        except requests.exceptions.RequestException as e:
            raise HTTPRequestException(e.message)

        if req.status_code != 200:
            raise HTTPRequestException(req.status_code)

            try:
                if 'stream' in requests_opts:
                    def stream():
                        for line in req.iter_lines():
                            # Handle byte arrays in Python 3
                            line = line.decode('utf-8')
                            if line:
                                yield json.loads(line)
                    rsp = stream
                elif self.api == 'export' and req.text.find('\n') > -1:
                    rsp = [json.loads(i) for i in req.text.split('\n')[0:-1]]
                else:
                    rsp = json.loads(req.text)
            except ValueError as e:
                raise ParseException(e.message)

        types_ = int, bool, basestring, types.FunctionType
        if not isinstance(rsp, types_) and 'error' in rsp and 'code' in rsp:
            try:
                Err = exception_for_code(rsp['code'])
            except KeyError:
                raise SystemException(rsp['error'])
            raise Err(rsp['error'])

        return rsp

    def __getattr__(self, method_name):
        def get(self, *args, **kwargs):
            params = dict((i, j) for (i, j) in enumerate(args))
            params.update(kwargs)
            # Some mandrill functions use - in the name
            return self.call(method_name.replace('_', '-'), params)

        return get.__get__(self)


def flatten_data(data, parent_key=''):
    items = []
    for k, v in data.items():
        new_key = ('%s[%s]' % (parent_key, k)) if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_data(v, new_key).items())
        elif isinstance(v, collections.MutableSequence):
            new_v = []
            for v_item in v:
                new_v.append((len(new_v), v_item))
            items.extend(flatten_data(dict(new_v), new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)
