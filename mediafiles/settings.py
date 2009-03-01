import os

from django.conf import settings


__all__ = ('DIRNAME', 'MEDIAFILES_DIRS_BLACKLIST', 'MEDIAFILES_EXTS_BLACKLIST',
           'MEDIAFILES_FILES_BLACKLIST', 'MEDIAFILES_IMAGES',
           'MEDIAFILES_MEDIA_PREFIX', 'MEDIAFILES_MEDIA_ROOT',
           'MEDIAFILES_PYGMENTS_STYLE', 'MEDIAFILES_ROOT', 'MEDIAFILES_URL')

# Absolute path to current directory
DIRNAME = os.path.abspath(os.path.dirname(__file__))

# List of blacklisted directory names. Your values will be extended by
# names used in urls, like ``mkdir``, ``properties``, etc.
MEDIAFILES_DIRS_BLACKLIST = list(getattr(settings,
                                         'MEDIAFILES_DIRS_BLACKLIST',
                                         []))
MEDIAFILES_DIRS_BLACKLIST.extend((
    'edit', 'logout', 'mkdir', 'mkfile', 'properties', 'rename', 'remove',
    'upload'
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

# Hide all **SCM** (``.git``, ``.svn`` and other) directories from explorer.
MEDIAFILES_HIDE_SCM_DIRS = getattr(settings, 'MEDIAFILES_HIDE_SCM_DIRS', True)

if MEDIAFILES_HIDE_SCM_DIRS:
    MEDIAFILES_DIRS_BLACKLIST.extend(('.bzr',
                                      'CVS',
                                      '_darcs',
                                      '.git',
                                      '.hg',
                                      '.svn'))

# List of image mimetypes.
MEDIAFILES_IMAGES = list(getattr(settings,
                                 'MEDIAFILES_IMAGES',
                                 ['image/bmp', 'image/gif', 'image/jpeg',
                                  'image/png',]))

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

# Setup this variable manually only if you want to manage files that not
# placed in your project's ``MEDIA_ROOT`` setting.
MEDIAFILES_ROOT = getattr(settings, 'MEDIAFILES_ROOT', settings.MEDIA_ROOT)

# Setup this variable manually only if you want to manage files that not
# placed in your project's ``MEDIA_ROOT`` setting.
MEDIAFILES_URL = getattr(settings, 'MEDIAFILES_URL', settings.MEDIA_URL)

# **Pygments** settings
# Name of Pygments style used for code highlighting. You can use one of:
#
#     ['manni', 'perldoc', 'borland', 'colorful', 'default', 'murphy',
#      'vs', 'trac', 'tango', 'fruity', 'autumn', 'bw', 'emacs', 'pastie',
#      'friendly', 'native']
MEDIAFILES_PYGMENTS_STYLE = getattr(settings,
                                    'MEDIAFILES_PYGMENTS_STYLE',
                                    'default')
