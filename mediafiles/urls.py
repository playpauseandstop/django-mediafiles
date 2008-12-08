from django.conf import settings
from django.conf.urls.defaults import *

from settings import *


if settings.DEBUG:
    urlpatterns = patterns('django.views.static',
        url(r'^%s/(?P<path>.*)' % MEDIAFILES_MEDIA_PREFIX.strip('/'), 'serve',
         {'document_root': MEDIAFILES_MEDIA_ROOT, 'show_indexes': False},
         name='mediafiles_media'),
    )
else:
    urlpatterns = patterns('')

urlpatterns += patterns('mediafiles.views',
    url(r'^mkdir/(?P<path>.*)$', 'mkdir', name='mediafiles_mkdir'),
    url(r'^properties/(?P<path>.*)$', 'properties',
        name='mediafiles_properties'),
    url(r'^remove/(?P<path>.*)$', 'remove', name='mediafiles_remove'),
    url(r'^rename/(?P<path>.*)$', 'rename', name='mediafiles_rename'),
    url(r'^upload/(?P<path>.*)$', 'upload', name='mediafiles_upload'),
    url(r'^(?P<path>.*)$', 'explorer', name='mediafiles_explorer'),
)
