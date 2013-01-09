MailSnake
=========

`MailSnake` is a Python wrapper for MailChimp's The API, STS API, Export API, and the
new Mandrill API. (Now with support for Python 3)

Installation
------------
    pip install mailsnake

Usage
-----

```python
from mailsnake import MailSnake
from mailsnake.exceptions import *

ms = MailSnake('YOUR MAILCHIMP API KEY')
try:
    ms.ping() # returns "Everything's Chimpy!"
except MailSnakeException:
    print 'An error occurred. :('
```

You can also catch specific errors:

```python
ms = MailSnake('my_wrong_mailchimp_api_key_that_does_not_exist')
try:
    ms.ping() # returns "Everything's Chimpy!"
except InvalidApiKeyException:
    print 'You have a bad API key, sorry.'
```
The default API is MCAPI, but STS, Export, and Mandrill can be used by
supplying an api argument set to 'sts', 'export', or 'mandrill'
respectively. Here's an example:

```python
mcsts = MailSnake('YOUR MAILCHIMP API KEY', api='sts')
mcsts.GetSendQuota() # returns something like {'Max24HourSend': '10000.0', 'SentLast24Hours': '0.0', 'MaxSendRate': '5.0'}
```

Since the Mandrill API is divided into sections, one must take that into
account when using it. Here's an example:

```python
mapi = MailSnake('YOUR MANDRILL API KEY', api='mandrill')
mapi.users.ping() # returns 'PONG!'
```

or:

```python
mapi_users = MailSnake('YOUR MANDRILL API KEY', api='mandrill', api_section='users')
mapi_users.ping() # returns 'PONG!'
```

Some Mandrill functions have a dash(-) in the name. Since Python
function names can't have dashes in them, use underscores(\_) instead:

```python
mapi = MailSnake('YOUR MANDRILL API KEY', api='mandrill')
mapi.messages.send(message={'html':'email html', 'subject':'email subject', 'from_email':'from@example.com', 'from_name':'From Name', 'to':[{'email':'to@example.com', 'name':'To Name'}]}) # returns 'PONG!'
```

Additional Request Options
--------------------------

MailSnake uses [Requests](http://docs.python-requests.org/en/v1.0.0/) for
HTTP. If you require more control over how your request is made,
you may supply a dictionary as the value of `requests_opts` when
constructing an instance of `MailSnake`. This will be passed through (as
kwargs) to `requests.post()`. See the next section for an example.

Streamed Responses
------------------

Since responses from the MailChimp Export API can be quite large, it is
helpful to be able to consume them in a streamed fashion. If you supply
`requests_opts={'stream': True}` when calling MailSnake, a generator is
returned that deserializes and yields each line of the streamed response
as it arrives:

```python
from mailsnake import MailSnake

opts = {'stream': True}
export = MailSnake('YOURAPIKEY', api='export', requests_opts=opts)
resp = export.list(id='YOURLISTID')

lines = 0
for list_member in resp():
    if lines > 0: # skip header row
        print list_member
    lines += 1
```

If you are using Requests < 1.0.0, supply `{'prefetch': False}` instead of
`{'stream': True}`.

Note
----

API parameters must be passed by name. For example:

```python
mcapi.listMemberInfo(id='YOUR LIST ID', email_address='name@example.com')
```

API Documentation
-----------------

Note that in order to use the STS API or Mandrill you first need to
enable the Amazon Simple Email Service or the Mandrill
[integration](https://us4.admin.mailchimp.com/account/integrations/ "MailChimp Integrations")
in MailChimp.

[MailChimp API v1.3 documentation](http://apidocs.mailchimp.com/api/1.3/ "MCAPI v1.3 Documentation")

[MailChimp STS API v1.0 documentation](http://apidocs.mailchimp.com/sts/1.0/ "STS API v1.0 Documentation")

[MailChimp Export API v1.0 documentation](http://apidocs.mailchimp.com/export/1.0/ "Export API v1.0")
