from pygments.formatters import HtmlFormatter

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page

from decorators import *
from forms import *
from settings import MEDIAFILES_PYGMENTS_STYLE
from utils import auto_context


def copy(request, path):
    pass
copy = staff_member_required(copy)
copy = path_process(copy)

def edit(request, path):
    context = auto_context(**locals())

    if not path.exists():
        return render_to_response('mediafiles/404.html', context)

    if not path.is_readable():
        return render_to_response('mediafiles/403.html', context)

    if path.is_dir():
        return HttpResponseRedirect(reverse('mediafiles_rename',
                                            kwargs={'path': path}))

    continue_editing = request.POST.get('_continue', False)

    if continue_editing:
        redirect_to = request.path
    else:
        redirect_to = request.REQUEST.get('next', None)
        if redirect_to is None or ' ' in redirect_to or '\\' in redirect_to:
            redirect_to = path.get_absolute_url()

    if request.method == 'POST':
        form = EditFileForm(request.POST, path=path)
        if form.is_valid():
            return HttpResponseRedirect(redirect_to)
    else:
        form = EditFileForm(path=path)

    context.update({'form': form})
    return render_to_response('mediafiles/edit.html', context)
edit = staff_member_required(edit)
edit = path_process(edit)

def explorer(request, path):
    context = auto_context(**locals())

    if not path.exists():
        return render_to_response('mediafiles/404.html', context)

    if not path.is_readable():
        return render_to_response('mediafiles/403.html', context)

    return render_to_response('mediafiles/explorer.html', context)
explorer = staff_member_required(explorer)
explorer = path_process(explorer)

def logout(request):
    return auth_views.logout(request)

def move(request, path):
    pass
move = staff_member_required(move)
move = path_process(move)

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
mkdir = staff_member_required(mkdir)
mkdir = path_process(mkdir)

def mkfile(request, path):
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
        form = MakeFileForm(request.POST, path=path)
        if form.is_valid():
            return HttpResponseRedirect(redirect_to)
    else:
        form = MakeFileForm(path=path)

    context.update({'form': form})
    return render_to_response('mediafiles/mkfile.html', context)
mkfile = staff_member_required(mkfile)
mkfile = path_process(mkfile)

def pygments_css(request):
    formatter = HtmlFormatter(nobackground=True,
                              style=MEDIAFILES_PYGMENTS_STYLE)

    response = HttpResponse("@charset 'utf-8';\n", mimetype='text/css')
    response.write(formatter.get_style_defs('.highlight'))

    return response
pygments_css = cache_page(pygments_css, 86400)

def remove(request, path):
    context = auto_context(**locals())

    if path.is_root():
        return HttpResponseRedirect(path.get_absolute_url())

    if not path.exists():
        return render_to_response('mediafiles/404.html', context)

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
remove = staff_member_required(remove)
remove = path_process(remove)

def rename(request, path):
    context = auto_context(**locals())

    if path.is_root():
        return HttpResponseRedirect(path.get_absolute_url())

    if not path.exists():
        return render_to_response('mediafiles/404.html', context)

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
rename = staff_member_required(rename)
rename = path_process(rename)

def upload(request, path):
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
        form = UploadForm(request.POST, request.FILES, path=path)
        if form.is_valid():
            return HttpResponseRedirect(redirect_to)
    else:
        form = UploadForm(path=path)

    context.update({'form': form})
    return render_to_response('mediafiles/upload.html', context)
upload = staff_member_required(upload)
upload = path_process(upload)
