import mimetypes
import os
import shutil
import sys

from datetime import datetime
from urlparse import urljoin

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.urlresolvers import reverse
from django.db.models import permalink
from django.template import Context, RequestContext
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _

from settings import MEDIAFILES_MEDIA_PREFIX


__all__ = ('auto_context', 'get_last_commit', 'get_media_prefix', 'get_version')

__commit = None

def auto_context(request=None, path=None):
    if request:
        return RequestContext(request, {'media_prefix': get_media_prefix(),
                                        'path': path,
                                        'version': get_version(),
                                        'version_commit': get_last_commit()})
    else:
        return Context({'media_prefix': get_media_prefix(),
                        'path': path,
                        'version': get_version(),
                        'version_commit': get_last_commit()})

def get_last_commit():
    global __commit
    if __commit is not None:
        return __commit

    from settings import DIRNAME
    git = os.path.abspath(os.path.join(DIRNAME, '../.git/logs/HEAD'))

    if not os.path.isfile(git):
        return None

    fr = open(git, 'r')
    lines = fr.readlines()
    __commit = lines[len(lines) - 1].split(' ')[1]
    fr.close()

    return __commit

def get_media_prefix():
    if settings.DEBUG and not MEDIAFILES_MEDIA_PREFIX.startswith('/'):
        return reverse('mediafiles_media', args=[''])
    return MEDIAFILES_MEDIA_PREFIX

def get_version():
    from . import VERSION
    if len(VERSION) == 2:
        return u'%s.%s' % (VERSION[0], VERSION[1])

    commit = get_last_commit()
    if commit is None:
        return u'%s.%s-%s' % (VERSION[0], VERSION[1], VERSION[2])

    return u'%s.%s-%s-%s' % (VERSION[0], VERSION[1], VERSION[2], commit)
