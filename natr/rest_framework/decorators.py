def patch_serializer_class(serializer_class):

    def decorator(fn):
        def wrapper(self, request, *a, **kw):
            prev_serializer_class = self.serializer_class
            self.serializer_class = serializer_class
            rv = fn(self, request, *a, **kw)
            self.serializer_class = prev_serializer_class
            return rv
        return wrapper
    return decorator


def ignore_permissions(fn):

    def wrapper(view, request, *a, **kw):
        view._ignore_permissions = True
        return fn(view, request, *a, **kw)
    
    return wrapper
