from django.conf import settings


# Cache timeout in seconds.
AMAZON_CACHE_TIMEOUT = getattr(settings, 'DHEAD_AMAZON_CACHE_TIMEOUT', 5 * 60)
