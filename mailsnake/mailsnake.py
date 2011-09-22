import urllib2
import urllib
try:
    import simplejson as json
except ImportError:
    import json

class MailSnake(object):

    dc = 'us1'
    base_api_url = 'https://%(dc)s.api.mailchimp.com/1.3/?method=%(method)s'

    def __init__(self, apikey = '', extra_params = {}):
        """
            Cache API key and address.
        """
        self.apikey = apikey

        self.default_params = {'apikey':apikey}
        self.default_params.update(extra_params)

        if '-' in self.apikey:
            self.dc = self.apikey.split('-')[1]

    def call(self, method, params = {}):
        url = self.base_api_url%{'dc': self.dc, 'method': method}
        params.update(self.default_params)

        post_data = urllib2.quote(json.dumps(params))
        headers={'Content-Type': 'application/json'}
        request = urllib2.Request(url, post_data, headers)
        response = urllib2.urlopen(request)

        return json.loads(response.read())

    def __getattr__(self, method_name):

        def get(self, *args, **kwargs):
            params = dict((i,j) for (i,j) in enumerate(args))
            params.update(kwargs)
            return self.call(method_name, params)

        return get.__get__(self)

class MailSnakeSTS(MailSnake):
    base_api_url = 'http://%(dc)s.sts.mailchimp.com/1.0/%(method)s'

    def _url_encode(self, data):
        def _(value):
            try:
                val = str(value).encode('utf-8')
            except:
                val = value.encode('utf-8')

            return urllib.quote(val)

        return '&'.join([ v for val in [[ "%s[%s]=%s"%(k,ik, _(iv)) for ik, iv in v.items()] if type(v)==dict else ["%s=%s"%(k,_(v))] for k,v in data.items() ] for v in val ])

    def call(self, method, params={}, headers = {}):
        url = self.base_api_url%{'dc': self.dc, 'method': method}
        params.update(self.default_params)

        post_data = self._url_encode(params)
        request = urllib2.Request(url, post_data, headers)
        response = urllib2.urlopen(request)

        return json.loads(response.read())

