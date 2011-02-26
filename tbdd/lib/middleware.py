from django.conf import settings
from django.contrib.sites.models import Site


class SiteDetectionMiddleware(object):

    def process_request(self, request):
        settings.SITE_THREAD_INFO.SITE_ID = 1   # Default.
        host = request.META.get('HTTP_HOST')
        if host:
            try:
                site = Site.objects.get(domain=host)
            except Site.DoesNotExist:
                pass
            else:
                settings.SITE_THREAD_INFO.SITE_ID = site.id
