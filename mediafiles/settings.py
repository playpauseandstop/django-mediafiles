import os
from django.conf import settings

# Absolute path to current directory
DIRNAME = os.path.abspath(os.path.dirname(__file__))

# URL prefix to ``django-mediafiles`` media directory. Similar to
# ``ADMIN_MEDIA_PREFIX`` settings value.
MEDIAFILES_MEDIA_PREFIX = getattr(settings,
                                  'MEDIAFILES_MEDIA_PREFIX',
                                  '/media/mediafiles')

# If Debug mode of your project enabled you can only customize this setting
# in settings file and ``django-mediafiles`` auto serve its static content
# by ``django.views.static.serve`` method
MEDIAFILES_MEDIA_ROOT = getattr(settings,
                                'MEDIAFILES_MEDIA_ROOT',
                                os.path.join(DIRNAME, 'media'))
