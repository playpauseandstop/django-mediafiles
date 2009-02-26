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


__all__ = ('Path', 'auto_context', 'get_last_commit', 'get_media_prefix',
           'get_version', 'permval')

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
    from settings import MEDIAFILES_MEDIA_PREFIX
    if settings.DEBUG and MEDIAFILES_MEDIA_PREFIX[0] != '/':
        return reverse('mediafiles_media', args=(), kwargs={'path': ''})
    return MEDIAFILES_MEDIA_PREFIX

def get_version():
    from . import VERSION
    if len(VERSION) == 2:
        return u'%s.%s' % (VERSION[0], VERSION[1])

    commit = get_last_commit()
    if commit is None:
        return u'%s.%s-%s' % (VERSION[0], VERSION[1], VERSION[2])

    return u'%s.%s-%s-%s' % (VERSION[0], VERSION[1], VERSION[2], commit)

class Path(object):
    def __init__(self, path, root):
        self.__root = root
        self.media_url = path.strip('/')
        self.safe_path = '/%s' % path.strip('/')

        if not path or path == '/':
            path = ''
        self.path = os.path.join(root, path)
        self.url = os.path.basename(self.path.rstrip('/'))
        self.name = self.url

        if self.safe_path != '/' and self.is_dir():
            self.media_url += '/'
            self.safe_path += '/'
            self.url += '/'

    def __repr__(self):
        if self.is_dir():
            return '<Directory "%s">' % self.path
        elif self.is_link():
            return '<Link "%s -> %s">' % (self.path, self.link)
        else:
            return '<File "%s">' % self.path

    def __str__(self):
        return self.url

    def __unicode__(self):
        return force_unicode(self.url)

    def _get_atime(self):
        assert self.exists(), 'This attribute allowed only for exists pathes.'
        if not hasattr(self, '__stat'):
            self.__stat = os.stat(self.path)
        return datetime.fromtimestamp(self.__stat.st_atime)
    atime = property(_get_atime)

    def _get_content(self):
        assert self.exists(), 'This attribute allowed only for exists pathes.'
        if not hasattr(self, '__content'):
            fr = open(self.path)
            content = fr.read()
            fr.close()
            setattr(self, '__content', content)
        return getattr(self, '__content')
    content = property(_get_content)

    def _get_content_type(self):
        if not hasattr(self, '__content_type'):
            content_type = mimetypes.guess_type(self.name)[0]
            if content_type is None:
                content_type = _('unknown')
            setattr(self, '__content_type', content_type)
        return getattr(self, '__content_type')
    content_type = property(_get_content_type)

    def _get_ctime(self):
        assert self.exists(), 'This attribute allowed only for exists pathes.'
        if not hasattr(self, '__stat'):
            self.__stat = os.stat(self.path)
        return datetime.fromtimestamp(self.__stat.st_ctime)
    ctime = property(_get_ctime)

    def exists(self):
        return self.is_dir() or self.is_file()

    def _get_extension(self):
        return os.path.splitext(self.name)[1]
    extension = property(_get_extension)

    def get_absolute_url(self):
        return ('mediafiles_explorer', (), {'path': self.safe_path.lstrip('/')})
    get_absolute_url = permalink(get_absolute_url)

    def get_edit_url(self):
        return ('mediafiles_edit', (), {'path': self.safe_path.lstrip('/')})
    get_edit_url = permalink(get_edit_url)

    def get_media_url(self):
        return urljoin(settings.MEDIA_URL, self.safe_path.lstrip('/'))

    def get_mkdir_url(self):
        return ('mediafiles_mkdir', (), {'path': self.safe_path.lstrip('/')})
    get_mkdir_url = permalink(get_mkdir_url)

    def get_mkfile_url(self):
        return ('mediafiles_mkfile', (), {'path': self.safe_path.lstrip('/')})
    get_mkfile_url = permalink(get_mkfile_url)

    def get_remove_url(self):
        return ('mediafiles_remove', (), {'path': self.safe_path.lstrip('/')})
    get_remove_url = permalink(get_remove_url)

    def get_rename_url(self):
        return ('mediafiles_rename', (), {'path': self.safe_path.lstrip('/')})
    get_rename_url = permalink(get_rename_url)

    def get_parent_url(self):
        return self.parent.get_absolute_url()

    def get_upload_url(self):
        return ('mediafiles_upload', (), {'path': self.safe_path.lstrip('/')})
    get_upload_url = permalink(get_upload_url)

    def is_dir(self):
        return os.path.isdir(self.path)

    def is_executeable(self):
        return os.access(self.path, os.X_OK)

    def is_link(self):
        return False

    def is_file(self):
        return os.path.isfile(self.path)

    def is_readable(self):
        return os.access(self.path, os.R_OK)

    def is_root(self):
        return self.path == self.__root

    def is_writeable(self):
        return os.access(self.path, os.W_OK)

    def list_dir(self, filter=None, order=None, desc=None):
        if not self.is_dir():
            raise TypeError, '%r is not a valid directory path.' % self.path

        filter = filter or 'all'
        if filter not in ('all', 'dirs', 'files', 'links'):
            filter = 'all'

        data = os.listdir(self.path)
        dirs, files = [], []
        for i, path in enumerate(data):
            path = force_unicode(path)
            path = os.path.join(self.safe_path, path).lstrip('/')
            path = Path(path, self.__root)
            if path.is_dir() and filter in ('all', 'dirs'):
                dirs.append(path)
            elif filter not in ('dirs',):
                files.append(path)

        sort_cmp = lambda x,y: cmp(force_unicode(x).lower(),
                                   force_unicode(y).lower())
        dirs.sort(sort_cmp), files.sort(sort_cmp)
        return dirs + files

    def mkdir(self, name):
        path = Path(name, self.path)
        if not path.exists() and not path.is_dir():
            os.mkdir(path.path)
        return path

    def mkfile(self, name, content):
        path = Path(name, self.path)

        if not path.exists() and not path.is_file():
            fw = open(path.path, 'w+')
            fw.write(content)
            fw.close()

        return path

    def _get_mtime(self):
        assert self.exists(), 'This attribute allowed only for exists pathes.'
        if not hasattr(self, '__stat'):
            self.__stat = os.stat(self.path)
        return datetime.fromtimestamp(self.__stat.st_mtime)
    mtime = property(_get_mtime)

    def _get_parent(self):
        if self.is_root():
            return None

        if hasattr(self, '__parent_cache'):
            return getattr(self, '__parent_cache')

        parts = self.safe_path.strip('/').split('/')
        if len(parts) == 1:
            parent = Path('', self.__root)
        else:
            parent = Path('/'.join(parts[:-1]), self.__root)
        setattr(self, '__parent_cache', parent)
        return parent
    parent = property(_get_parent)

    def _get_parts(self):
        if self.is_root():
            return []

        if hasattr(self, '__parts_cache'):
            return getattr(self, '__parts_cache')

        parts = self.safe_path.strip('/').split('/')
        result = []
        for i, p in enumerate(parts):
            p = '/'.join(parts[:i + 1])
            result.append(Path(p, self.__root))
        setattr(self, '__parts_cache', result)
        return result
    parts = property(_get_parts)

    def remove(self):
        if self.is_dir():
            shutil.rmtree(self.path)
        else:
            os.remove(self.path)

    def rename(self, newname):
        newpath = Path(newname, self.parent.path)
        shutil.move(self.path, newpath.path)
        return newpath

    def _get_size(self):
        if self.is_dir():
            if hasattr(self, '__size_cache'):
                return getattr(self, '__size_cache')
            setattr(self, '__size_cache', self._get_dir_size())
            return getattr(self, '__size_cache')
        return os.path.getsize(self.path)
    size = property(_get_size)

    def upload(self, file):
        assert self.is_dir(), 'Can not upload file to not a directory.'
        assert isinstance(file, UploadedFile), \
               'Only upload of UploadedFile objects was accepted.'

        path = Path(file.name, self.path)
        fw = open(path.path, 'wb+')

        for chunk in file.chunks():
            fw.write(chunk)

        fw.close()
        return path

    def write(self, content):
        assert self.is_file(), 'Can not write content to not a file.'

        fw = open(self.path, 'wb+')
        fw.write(content)
        fw.close()

        return self

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
