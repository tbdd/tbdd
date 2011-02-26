from django.conf.urls.defaults import *


urlpatterns = patterns('tbdd.apps.dhead.views',
    url(regex=  r'^$',
        view=   'productlist',
        name=   'dhead_productlist',
    ),
    url(regex=  r'^about/$',
        view=   'about',
        name=   'dhead_about',
    ),
    url(regex=  r'^privacy/$',
        view=   'privacy',
        name=   'dhead_privacy',
    ),
    url(regex=  r'^(?P<keywords>[\w-]+)/$',
        view=   'productlist',
        name=   'dhead_productlist',
    ),
    url(regex=  r'^(?P<keywords>[\w-]+)/(?P<page>[\d]+)/$',
        view=   'productlist',
        name=   'dhead_productlist',
    ),
    url(regex=  r'^(?P<keywords>[\w-]+)/(?P<title_slug>[\w-]+)-(?P<asin>[\w]+)/$',
        view=   'productdetail',
        name=   'dhead_productdetail',
    ),
    url(regex=  r'^go/(?P<asin>[\w]+)/$',
        view=   'productgo',
        name=   'dhead_productgo',
    ),
)
