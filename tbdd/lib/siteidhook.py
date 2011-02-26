# http://djangosnippets.org/snippets/1099/

from threading import local


SITE_THREAD_INFO = local()


class SiteIdHook(object):

    def __int__(self):
        return SITE_THREAD_INFO.SITE_ID

    def __hash__(self):
        return SITE_THREAD_INFO.SITE_ID
