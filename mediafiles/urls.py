from django.conf import settings
from django.conf.urls.defaults import *

from settings import *


if settings.DEBUG and not MEDIAFILES_MEDIA_PREFIX.startswith('/'):
    urlpatterns = patterns('django.views.static',
        url(r'^%s/(?P<path>.*)' % MEDIAFILES_MEDIA_PREFIX.strip('/'), 'serve',
            {'document_root': MEDIAFILES_MEDIA_ROOT, 'show_indexes': False},
            name='mediafiles_media'),
    )
else:
    urlpatterns = patterns('')

urlpatterns += patterns('mediafiles.views',
    url(r'^copy/(?P<path>.*)$', 'copy', name='mediafiles_copy'),
    url(r'^edit/(?P<path>.*)$', 'edit', name='mediafiles_edit'),
    url(r'^logout/$', 'logout', name='mediafiles_logout'),
    url(r'^mkdir/(?P<path>.*)$', 'mkdir', name='mediafiles_mkdir'),
    url(r'^mkfile/(?P<path>.*)$', 'mkfile', name='mediafiles_mkfile'),
    url(r'^move/(?P<path>.*)$', 'move', name='mediafiles_move'),
    url(r'^pygments/css/$', 'pygments_css', name='mediafiles_pygments_css'),
    url(r'^remove/(?P<path>.*)$', 'remove', name='mediafiles_remove'),
    url(r'^rename/(?P<path>.*)$', 'rename', name='mediafiles_rename'),
    url(r'^upload/(?P<path>.*)$', 'upload', name='mediafiles_upload'),
    url(r'^(?P<path>.*)$', 'explorer', name='mediafiles_explorer'),
)
