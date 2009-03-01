import mimetypes
import os
import shutil

from datetime import datetime

from django.core.files.uploadedfile import UploadedFile
from django.db.models import permalink
from django.utils.encoding import force_unicode, smart_str
from django.utils.translation import ugettext as _

from settings import *


__all__ = ('Path',)

class Path(object):
    def __init__(self, path=None):
        self._is_root = False

        if path is not None:
            path = force_unicode(path)
        else:
            path = u''

        urlpath = path

        if path.startswith('/'):
            urlpath = path.lstrip('/')
        else:
            path = '/' + path

        if not urlpath:
            self._is_root = True

        self._abspath = os.path.join(MEDIAFILES_ROOT, urlpath)
        self._path = path
        self._urlpath = urlpath

        if self.is_dir() and not self.is_root() and not path.endswith('/'):
            self._abspath = self._abspath + '/'
            self._path = self._path + '/'
            self._urlpath = self._urlpath + '/'

    def __repr__(self):
        if self.is_dir():
            pattern = u"<Directory '%s'>"
        elif self.is_link():
            pattern = u"<Link '%s'>"
        elif self.is_file():
            pattern = u"<File '%s'>"
        else:
            pattern = u"<DoesNotExist '%s'>"

        return pattern % self._abspath

    def __str__(self):
        return smart_str(self._path)

    def __unicode__(self):
        return self._path

    def _get_abspath(self):
        return self._abspath
    abspath = property(_get_abspath)

    def _get_atime(self):
        assert self.exists(), 'Existed path expected.'

        if not hasattr(self, '__stat_cache'):
            setattr(self, '__stat_cache', os.stat(self._abspath))

        return datetime.fromtimestamp(getattr(self, '__stat_cache').st_atime)
    atime = property(_get_atime)

    def child(self, path):
        return Path(os.path.normpath(os.path.join(self._path, path)))

    def _get_childs(self, filter=None):
        assert self.is_dir(), 'Directory path expected.'

        filter = filter or 'all'
        if filter not in ('all', 'dirs', 'files'):
            filter = 'all'

        if not hasattr(self, '__childs_%s_cache' % filter):
            childs = []
            dirs, files = [], []

            for child in os.listdir(self._abspath):
                path = self.child(child)
                if path.is_dir():
                    if path.name in MEDIAFILES_DIRS_BLACKLIST:
                        continue
                    dirs.append(path)
                else:
                    if path.name in MEDIAFILES_FILES_BLACKLIST:
                        continue
                    files.append(path)

            sort_cmp = lambda x, y: cmp(x.name, y.name)
            dirs.sort(sort_cmp)
            files.sort(sort_cmp)

            setattr(self, '__childs_all_cache', dirs + files)
            setattr(self, '__childs_dirs_cache', dirs)
            setattr(self, '__childs_files_cache', files)

        return getattr(self, '__childs_%s_cache' % filter)
    childs = property(_get_childs)

    def _get_content(self):
        assert self.is_file(), 'File path expected.'

        if not hasattr(self, '__content_cache'):
            fr = open(self.abspath, 'rb+')
            content = force_unicode(fr.read())
            fr.close()
            setattr(self, '__content_cache', content)

        return getattr(self, '__content_cache')
    content = property(_get_content)

    def _get_content_type(self):
        if not hasattr(self, '__content_type_cache'):
            content_type = mimetypes.guess_type(self.name)[0]
            if content_type is None:
                content_type = _('unknown')
            setattr(self, '__content_type_cache', content_type)

        return getattr(self, '__content_type_cache')
    content_type = property(_get_content_type)

    def copy(self, newpath):
        assert not self.is_root(), 'Root path does not expected.'
        assert self.exists(), 'Existed path expected.'

        path = Path(newpath)

        if self.is_dir():
            shutil.copytree(self._abspath, path.abspath)
        else:
            shutil.copy(self._abspath, path.abspath)

        return path

    def _get_ctime(self):
        assert self.exists(), 'Existed path expected.'

        if not hasattr(self, '__stat_cache'):
            setattr(self, '__stat_cache', os.stat(self._abspath))

        return datetime.fromtimestamp(getattr(self, '__stat_cache').st_ctime)
    ctime = property(_get_ctime)

    def _get_dirs(self):
        return self._get_childs('dirs')
    dirs = property(_get_dirs)

    def exists(self):
        return os.path.exists(self._abspath)

    def _get_extension(self):
        if not hasattr(self, '__extension_cache'):
            unused, extension = os.path.splitext(self._path)
            setattr(self, '__extension_cache', extension)
        return getattr(self, '__extension_cache')
    extension = property(_get_extension)

    def _get_files(self):
        return self._get_childs('files')
    files = property(_get_files)

    def get_absolute_url(self):
        return ('mediafiles_explorer', [self._urlpath])
    get_absolute_url = permalink(get_absolute_url)

    def get_direct_url(self):
        return os.path.join(MEDIAFILES_URL, self.urlpath)

    def is_dir(self):
        return os.path.isdir(self._abspath)

    def is_executable(self):
        return os.access(self._abspath, os.X_OK)

    def is_file(self):
        return os.path.isfile(self._abspath)

    def is_link(self):
        return os.path.islink(self._abspath)

    def is_readable(self):
        return os.access(self._abspath, os.R_OK)

    def is_root(self):
        return self._is_root

    def is_writeable(self):
        return os.access(self._abspath, os.W_OK)

    def mkdir(self, name):
        assert self.is_dir(), 'Directory path expected.'

        path = self.child(name)
        os.mkdir(path.abspath)

        self._invalidate_cache(('childs_all', 'childs_dirs', 'size'))
        return path

    def mkfile(self, name, content):
        assert self.is_dir(), 'Directory path expected.'

        path = self.child(name)

        fw = open(path.abspath, 'wb+')
        fw.write(content)
        fw.close()

        self._invalidate_cache(('childs_all', 'childs_files', 'size'))
        return path

    def move(self, newpath):
        assert not self.is_root(), 'Root path does not expected.'
        assert self.exists(), 'Existed path expected.'

        path = Path(newpath)
        shutil.move(self._abspath, path.abspath)

        return path

    def _get_mtime(self):
        assert self.exists(), 'Existed path expected.'

        if not hasattr(self, '__stat_cache'):
            setattr(self, '__stat_cache', os.stat(self._abspath))

        return datetime.fromtimestamp(getattr(self, '__stat_cache').st_mtime)
    mtime = property(_get_mtime)

    def _get_name(self):
        if self._path.endswith('/'):
            return os.path.basename(self._path.rstrip('/'))
        return os.path.basename(self._path)
    name = property(_get_name)

    def _get_parent(self):
        if self.is_root():
            return None

        if not hasattr(self, '__parent_cache'):
            setattr(self, '__parent_cache', self.child('..'))

        return getattr(self, '__parent_cache')
    parent = property(_get_parent)

    def _get_parts(self):
        if self.is_root():
            return []

        if not hasattr(self, '__parts_cache'):
            parts = []
            path_parts = self._path.split('/')

            for i, part in enumerate(path_parts):
                if i == len(path_parts) - 1 and self.is_dir():
                    break

                if not len(parts):
                    path = Path(part)
                else:
                    last = parts[-1]
                    path = Path(os.path.join(last.urlpath, part))

                parts.append(path)

            setattr(self, '__parts_cache', parts)

        return getattr(self, '__parts_cache')
    parts = property(_get_parts)

    def _get_path(self):
        return self._path
    path = property(_get_path)

    def refresh(self):
        self._invalidate_cache()
        return self

    def remove(self):
        assert not self.is_root(), 'Root path does not expected.'
        assert self.exists(), 'Existed path expected.'

        if self.is_dir():
            shutil.rmtree(self._abspath)
        else:
            os.remove(self._abspath)

        self._invalidate_cache()
        return None

    def rename(self, newname):
        assert not self.is_root(), 'Root path does not expected.'
        assert self.exists(), 'Existed path expected.'

        path = self.parent.child(newname)
        shutil.move(self._abspath, path.abspath)

        self.__init__(path.path)
        self._invalidate_cache()
        return self

    def _get_size(self):
        assert self.exists(), 'Existed path expected.'

        if self.is_dir():
            if not hasattr(self, '__size_cache'):
                setattr(self, '__size_cache', self._get_dir_size())
            return getattr(self, '__size_cache')

        return os.path.getsize(self.abspath)
    size = property(_get_size)

    def upload(self, file):
        assert self.is_dir(), 'Directory path expected.'
        assert isinstance(file, UploadedFile), 'UploadedFile instance expected.'

        path = self.child(file.name)
        fw = open(path.abspath, 'wb+')

        for chunk in file.chunks():
            fw.write(chunk)

        fw.close()
        return path

    def _get_urlpath(self):
        return self._urlpath
    urlpath = property(_get_urlpath)

    def write(self, content, mode=None):
        assert self.is_file(), 'File path expected.'

        mode = mode or 'wb+'
        fw = open(self.abspath, mode)
        fw.write(content)
        fw.close()

        self._invalidate_cache('size')
        return self

    def _get_dir_size(self, abspath=None):
        abspath = abspath or self._abspath

        if not os.path.isdir(abspath):
            return os.path.getsize(abspath)

        result = 0L
        for root, dirs, files in os.walk(abspath):
            for f in files:
                f = os.path.join(root, f)
                result += os.path.getsize(f)
        return result

    def _invalidate_cache(self, attr_data=None):
        for attr in dir(self):
            if not attr.startswith('__') or not attr.endswith('_cache'):
                continue

            if attr_data is not None:
                attr_slug = attr[2:-6]

                if isinstance(attr_data, (list, tuple)):
                    if not attr_slug in attr_data:
                        continue
                else:
                    if attr_slug != attr_data:
                        continue

            delattr(self, attr)
