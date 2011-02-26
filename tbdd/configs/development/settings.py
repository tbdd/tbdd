from tbdd.configs.common.settings import *


CACHE_BACKEND = 'locmem://'


# Enable debug toolbar.

try:
    import debug_toolbar
except ImportError:
    pass
else:
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    from fnmatch import fnmatch
    class glob_list(list):
        def __contains__(self, key):
            for elt in self:
                if fnmatch(key, elt): return True
            return False
    INTERNAL_IPS = glob_list([
        '*.*.*.*',
    ])
