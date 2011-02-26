from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(regex=  r'^admin/doc/',
        view=   include('django.contrib.admindocs.urls'),
    ),
    url(regex=  r'^admin/',
        view=   include(admin.site.urls),
    ),
    url(regex=  r'^assets/(?P<path>.*)$',
        view=   'django.views.static.serve',
        kwargs= dict(
            document_root=settings.MEDIA_ROOT,
        ),
    ),
    url(regex=  r'',
        view=   include('tbdd.apps.dhead.urls'),
    ),
)
