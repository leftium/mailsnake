#!/usr/bin/env python
import re, sys
from setuptools import setup, find_packages

# dep sugar.
_ver = sys.version_info

if _ver[0] == 2:
    dep = ['simplejson', 'requests']
elif _ver[0] == 3:
    dep = ['requests']

msinit = open('mailsnake/__init__.py').read()
author = re.search("__author__ = '([^']+)'", msinit).group(1)
version = re.search("__version__ = '([^']+)'", msinit).group(1)

setup(
    name='mailsnake',
    version=version,
    description='MailChimp API v1.3 wrapper for Python.',
    long_description=open('README.rst').read(),
    author=author,
    url='https://github.com/michaelhelmick/python-mailsnake',
    packages=find_packages(),
    download_url='http://pypi.python.org/pypi/mailsnake/',
    keywords='mailsnake mailchimp api wrapper 1.3',
    zip_safe=True,
    install_requires=dep,
    py_modules=['mailsnake'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
