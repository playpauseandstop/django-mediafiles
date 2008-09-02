from django.shortcuts import render_to_response
from django.template import RequestContext

from decorators import *
from utils import get_media_prefix, get_version

def explorer(request, path):
    context = RequestContext(request, {'media_prefix': get_media_prefix(),
                                       'path': path,
                                       'version': get_version()})
    if not path.exists():
        return render_to_response('mediafiles/404.html', context)
    return render_to_response('mediafiles/explorer.html', context)
explorer = path_process(explorer)
