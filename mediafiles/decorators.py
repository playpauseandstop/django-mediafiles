from path import *


__all__ = ('path_process',)

def path_process(view_func):
    def _wrapper(request, *args, **kwargs):
        if not kwargs:
            if not len(args):
                return view_func(request, *args, **kwargs)
            args[0] = Path(args[0])
        else:
            if not 'path' in kwargs:
                return view_func(request, *args, **kwargs)
            kwargs['path'] = Path(kwargs['path'])
        return view_func(request, *args, **kwargs)
    return _wrapper
