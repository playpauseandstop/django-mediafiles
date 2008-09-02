import os, sys

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import permalink

__all__ = ('Path', 'get_media_prefix', 'get_version')

def get_media_prefix():
    from settings import MEDIAFILES_MEDIA_PREFIX
    if settings.DEBUG and MEDIAFILES_MEDIA_PREFIX[0] != '/':
        return reverse('mediafiles_media', args=(), kwargs={'path': ''})
    return MEDIAFILES_MEDIA_PREFIX

def get_version():
    from . import VERSION
    if len(VERSION) == 2:
        return '%s.%s'

    from settings import DIRNAME
    git = os.path.abspath(os.path.join(DIRNAME, '../.git/logs/HEAD'))

    if not os.path.isfile(git):
        return '%s.%s-%s' % (VERSION[0], VERSION[1], VERSION[2])

    fr = open(git, 'r')
    lines = fr.readlines()
    commit = lines[len(lines) - 1].split(' ')[0]
    fr.close()

    return '%s.%s-%s-%s' % (VERSION[0], VERSION[1], VERSION[2], commit)

class Path(object):
    def __init__(self, path, root):
        self.__root = root
        self.media_url = path.strip('/')
        self.safe_path = '/%s' % path.strip('/')

        if not path or path == '/':
            path = ''
        self.path = os.path.join(root, path)
        self.url = os.path.basename(path)

        if self.safe_path != '/' and self.is_dir():
            self.media_url += '/'
            self.safe_path += '/'
            self.url += '/'

    def __str__(self):
        return self.url

    def __unicode__(self):
        if self.isdir():
            return u'Directory <%s>' % self.path
        elif self.islink():
            return u'Link <%s -> %s>' % (self.path, self.link)
        else:
            return u'File <%s>' % self.path

    def exists(self):
        return self.is_dir() or self.is_file()

    def get_absolute_url(self):
        return ('mediafiles_explorer', (), {'path': self.safe_path.lstrip('/')})
    get_absolute_url = permalink(get_absolute_url)

    def get_parent_url(self):
        parent = self.parent or ''
        return ('mediafiles_explorer', (), {'path': parent})
    get_parent_url = permalink(get_parent_url)

    def is_dir(self):
        return os.path.isdir(self.path)

    def is_link(self):
        return False

    def is_file(self):
        return os.path.isfile(self.path)

    def is_root(self):
        return self.path == self.__root

    def list_dir(self, order=None, desc=None):
        if not self.is_dir():
            raise TypeError, '<%s> is not a valid directory path.' % self.path
        data = os.listdir(self.path)
        dirs, files = [], []
        for i, path in enumerate(data):
            path = os.path.join(self.safe_path, path).lstrip('/')
            path = Path(path, self.__root)
            if path.is_dir():
                dirs.append(path)
            else:
                files.append(path)
        sort_cmp = lambda x,y: cmp(x.__str__().lower(), y.__str__().lower())
        dirs.sort(sort_cmp), files.sort(sort_cmp)
        return dirs + files

    def _get_parent(self):
        if self.is_root():
            return None
        parts = self.safe_path.strip('/').split('/')
        if len(parts) == 1:
            return ''
        return '/'.join(parts)
    parent = property(_get_parent)

    def _get_size(self):
        if self.is_dir():
            if hasattr(self, '__size_cache'):
                return getattr(self, '__size_cache')
            setattr(self, '__size_cache', self._get_dir_size())
            return getattr(self, '__size_cache')
        return os.path.getsize(self.path)
    size = property(_get_size)

    def _get_dir_size(self, path=None):
        path = path or self.path
        if not os.path.isdir(path):
            return os.path.getsize(path)
        result = 0L
        for root, dirs, files in os.walk(path):
            for f in files:
                f = os.path.join(root, f)
                result += os.path.getsize(f)
        return result
