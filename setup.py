#!/usr/bin/env python

import os
from distutils.core import setup


readme = open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r')
README = readme.read()
readme.close()

setup(
    name='django-mediafiles',
    version='0.2',
    description='Django media files manager',
    long_description=README,
    author='Igor Davydenko',
    author_email='playpauseandstop@gmail.com',
    url='http://code.google.com/p/django-mediafiles/',
    download_url='http://django-mediafiles.googlecode.com/files/django-mediafiles-0.2.zip',
    packages=['mediafiles', 'mediafiles.templatetags'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    keywords='django media files static',
)
