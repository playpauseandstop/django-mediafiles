import os

from django.conf import settings


__all__ = ('DIRNAME', 'MEDIAFILES_DIRS_BLACKLIST', 'MEDIAFILES_EXTS_BLACKLIST',
           'MEDIAFILES_FILES_BLACKLIST', 'MEDIAFILES_MEDIA_PREFIX',
           'MEDIAFILES_MEDIA_ROOT')

# Absolute path to current directory
DIRNAME = os.path.abspath(os.path.dirname(__file__))

# List of blacklisted directory names. Your values will be extended by
# names used in urls, like ``mkdir``, ``properties``, etc.
MEDIAFILES_DIRS_BLACKLIST = list(getattr(settings,
                                         'MEDIAFILES_DIRS_BLACKLIST',
                                         []))
MEDIAFILES_DIRS_BLACKLIST.extend((
    'mkdir', 'properties', 'rename', 'remove', 'upload'
))

# List of blacklisted file extensions. **Note**, add dot before extension,
# like ``.txt`` instead of ``txt``.
MEDIAFILES_EXTS_BLACKLIST = list(getattr(settings,
                                         'MEDIAFILES_EXTS_BLACKLIST',
                                         []))

# List of blacklisted file names.
MEDIAFILES_FILES_BLACKLIST = list(getattr(settings,
                                          'MEDIAFILES_FILES_BLACKLIST',
                                          []))

# URL prefix to ``django-mediafiles`` media directory. Similar to
# ``ADMIN_MEDIA_PREFIX`` settings value.
# **Note:** In Debug mode use relative prefix, e.g. ``mediafiles/`` not
# absolute, e.g. ``/media/mediafiles/``.
MEDIAFILES_MEDIA_PREFIX = getattr(settings,
                                  'MEDIAFILES_MEDIA_PREFIX',
                                  'mediafiles/')

# If Debug mode of your project enabled you can only customize this setting
# in settings file and ``django-mediafiles`` auto serve its static content
# by ``django.views.static.serve`` method
MEDIAFILES_MEDIA_ROOT = getattr(settings,
                                'MEDIAFILES_MEDIA_ROOT',
                                os.path.join(DIRNAME, 'media'))
