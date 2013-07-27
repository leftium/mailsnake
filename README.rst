MailSnake
=========

.. image:: https://badge.fury.io/py/mailsnake.png
        :target: http://badge.fury.io/py/mailsnake
.. image:: https://travis-ci.org/michaelhelmick/python-mailsnake.png?branch=master
        :target: https://travis-ci.org/michaelhelmick/python-mailsnake
.. image:: https://pypip.in/d/mailsnake/badge.png
        :target: https://crate.io/packages/mailsnake/

``MailSnake`` is a Python wrapper for `MailChimp API 1.3 <http://www.mailchimp.com/api/1.3/>`_ (as well as the `STS API <http://apidocs.mailchimp.com/sts/1.0/>`_, `Export API <http://apidocs.mailchimp.com/export/>`_, and `Mandrill API <http://mandrillapp.com/api/docs/>`_) (Now with support for Python 3)

Installation
------------

.. code-block:: bash

    $ pip install mailsnake

Usage
-----

Basic Ping
~~~~~~~~~~

.. code-block:: python

    from mailsnake import MailSnake
    from mailsnake.exceptions import *
    
    ms = MailSnake('YOUR MAILCHIMP API KEY')
    try:
        ms.ping() # returns "Everything's Chimpy!"
    except MailSnakeException:
        print 'An error occurred. :('

Mandrill Ping
~~~~~~~~~~~~~

.. code-block:: python

    mapi = MailSnake('YOUR MANDRILL API KEY', api='mandrill')
    mapi.users.ping() # returns "PONG!"


STS Example
~~~~~~~~~~~

.. code-block:: python

    mcsts = MailSnake('YOUR MAILCHIMP API KEY', api='sts')
    mcsts.GetSendQuota() # returns something like {'Max24HourSend': '10000.0', 'SentLast24Hours': '0.0', 'MaxSendRate': '5.0'}


Catching Errors
~~~~~~~~~~~~~~~

.. code-block:: python

    ms = MailSnake( 'my_wrong_mailchimp_api_key_that_does_not_exist')
    try:
        ms.ping() # returns "Everything's Chimpy!"
    except InvalidApiKeyException:
        print 'You have a bad API key, sorry.'

Note
----

API parameters must be passed by name. For example:

.. code-block:: python

    ms.listMemberInfo(id='YOUR LIST ID', email_address='name@email.com')
