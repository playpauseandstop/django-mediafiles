from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from decorators import *
from forms import *
from utils import auto_context

def chmod(request, path):
    pass

def chown(request, path):
    pass

def explorer(request, path):
    context = auto_context(**locals())
    if not path.exists():
        return render_to_response('mediafiles/404.html', context)
    return render_to_response('mediafiles/explorer.html', context)
explorer = path_process(explorer)

def mkdir(request, path):
    context = auto_context(**locals())

    if not path.exists() or not path.is_dir():
        return render_to_response('mediafiles/404.html', context)

    if not path.is_writeable():
        return render_to_response('mediafiles/403.html', context)

    add_another = request.REQUEST.get('_addanother', False)

    if add_another:
        redirect_to = request.path
    else:
        redirect_to = request.REQUEST.get('next', None)
        if redirect_to is None or ' ' in redirect_to or '\\' in redirect_to:
            redirect_to = path.get_absolute_url()

    if request.method == 'POST':
        form = MakeDirectoryForm(request.POST, path=path)
        if form.is_valid():
            return HttpResponseRedirect(redirect_to)
    else:
        form = MakeDirectoryForm(path=path)

    context.update({'form': form})
    return render_to_response('mediafiles/mkdir.html', context)
mkdir = path_process(mkdir)

def properties(request, path):
    pass

def remove(request, path):
    context = auto_context(**locals())

    if path.is_root():
        return HttpResponseRedirect(path.get_absolute_url())

    if not path.exists():
        return render_to_response('mediafiles/404.html', context)

    if not path.is_writeable():
        return render_to_response('mediafiles/403.html', context)

    redirect_to = request.REQUEST.get('next', None)

    if redirect_to is None or ' ' in redirect_to or '\\' in redirect_to:
        redirect_to = path.parent.get_absolute_url()

    if request.method == 'POST':
        form = RemovePathForm(request.POST, path=path)
        if form.is_valid():
            return HttpResponseRedirect(redirect_to)
    else:
        form = RemovePathForm(path=path)

    context.update({'form': form})
    return render_to_response('mediafiles/remove.html', context)
remove = path_process(remove)

def rename(request, path):
    context = auto_context(**locals())

    if path.is_root():
        return HttpResponseRedirect(path.get_absolute_url())

    if not path.exists():
        return render_to_response('mediafiles/404.html', context)

    if not path.is_writeable():
        return render_to_response('mediafiles/403.html', context)

    redirect_to = request.REQUEST.get('next', None)

    if redirect_to is None or ' ' in redirect_to or '\\' in redirect_to:
        redirect_to = path.parent.get_absolute_url()

    if request.method == 'POST':
        if not 'oldname' in request.POST:
            request.POST.update({'oldname': path.name})

        form = RenamePathForm(request.POST, path=path)
        if form.is_valid():
            return HttpResponseRedirect(redirect_to)
    else:
        form = RenamePathForm(initial={'oldname': path.name}, path=path)

    context.update({'form': form})
    return render_to_response('mediafiles/rename.html', context)
rename = path_process(rename)

def upload(request, path):
    context = auto_context(**locals())

    if not path.exists():
        return render_to_response('mediafiles/404.html', context)

    if not path.is_writeable():
        return render_to_response('mediafiles/403.html', context)

    add_another = request.REQUEST.get('_addanother', False)

    if add_another:
        redirect_to = request.path
    else:
        redirect_to = request.REQUEST.get('next', None)
        if redirect_to is None or ' ' in redirect_to or '\\' in redirect_to:
            redirect_to = path.get_absolute_url()

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, path=path)
        if form.is_valid():
            return HttpResponseRedirect(redirect_to)
    else:
        form = UploadForm(path=path)

    context.update({'form': form})
    return render_to_response('mediafiles/upload.html', context)
upload = path_process(upload)
