#!/usr/bin/env python

from setuptools import setup

__author__ = 'John-Kim Murphy'
__version__ = '2.0.0'

packages = [
    'mailsnake',
]

setup(
    name='mailsnake',
    version=__version__,
    install_requires=['requests==1.2.3'],
    author=__author__,
    license=open('LICENSE').read(),
    url='https://github.com/michaelhelmick/python-mailsnake',
    keywords='mailsnake mailchimp api wrapper export mandrill sts 1.3 p3k',
    description='MailChimp API v1.3, STS, Export, Mandrill wrapper for Python.',
    long_description=open('README.rst').read(),
    include_package_data=True,
    packages=packages,
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
