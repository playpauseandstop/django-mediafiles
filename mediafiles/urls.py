from django.conf import settings
from django.conf.urls.defaults import *

from settings import *

urlpatterns = patterns('mediafiles.views',
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^%s/(?P<path>.*)' % MEDIAFILES_MEDIA_PREFIX.strip('/'), 'serve',
         {'document_root': MEDIAFILES_MEDIA_ROOT, 'show_indexes': False}),
    )