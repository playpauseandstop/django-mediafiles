from django.conf import settings


__all__ = ('path_process',)

def path_process(view_func):
    from utils import Path
    def _wrapper(request, *args, **kwargs):
        if not kwargs:
            if not len(args):
                return view_func(request, *args, **kwargs)
            args[0] = Path(args[0], settings.MEDIA_ROOT)
        else:
            if not 'path' in kwargs:
                return view_func(request, *args, **kwargs)
            kwargs['path'] = Path(kwargs['path'], settings.MEDIA_ROOT)
        return view_func(request, *args, **kwargs)
    return _wrapper
