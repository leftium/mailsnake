#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='mailsnake',
    version='1.6.4',
    description='MailChimp API v1.3, STS, Export, Mandrill wrapper for Python.',
    long_description=open('README.rst').read(),
    author='John-Kim Murphy',
    url='https://github.com/michaelhelmick/python-mailsnake',
    packages=find_packages(),
    download_url='http://pypi.python.org/pypi/mailsnake/',
    keywords='mailsnake mailchimp api wrapper export mandrill sts 1.3 p3k',
    zip_safe=True,
    install_requires=['requests'],
    py_modules=['mailsnake'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
