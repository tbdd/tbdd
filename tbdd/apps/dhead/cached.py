from json import loads
from xml.etree.ElementTree import fromstring

import bottlenose
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.core.cache import cache
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.template.defaultfilters import slugify

from tbdd.apps.dhead.lib import deslugify
from tbdd.apps.dhead.models import Storefront
from tbdd.apps.dhead.settings import AMAZON_CACHE_TIMEOUT
from tbdd.apps.dhead.templatetags.dhead_tags import azasin
from tbdd.lib.awsecs import ECS_TAG


def _amazon(storefront):
    return bottlenose.Amazon(settings.ACCESS_KEY_ID, settings.SECRET_ACCESS_KEY, storefront.associate_tag)


def _keyprefix(storefront, keywords):
    return '{0}-{1}'.format(storefront.site.domain, slugify(keywords))


def amazon_lookup(storefront, asin):
    """Return an <Item> XML element based on an Amazon API search or lookup."""
    key = '{0}-azlookup-{1}'.format(storefront.site.domain, asin)
    value = cache.get(key)
    if value is not None:
        return value
    # Cache miss.
    az = _amazon(storefront)
    results = az.ItemLookup(
        ItemId=asin,
        ResponseGroup='Medium,OfferSummary,Reviews,Offers,VariationSummary',
    )
    results = fromstring(results)
    item = results.find(ECS_TAG('Items')).find(ECS_TAG('Item'))
    cache.set(key, item, AMAZON_CACHE_TIMEOUT)
    return item


def amazon_search(storefront, keywords, page):
    """Return a list of ASINs from a search against the Amazon API."""
    key = '{0}-{1}-azsearch-{2}'.format(storefront.site.domain, slugify(keywords), page)
    value = cache.get(key)
    if value is not None:
        return value
    # Cache miss.
    keywords = deslugify(keywords)
    az = _amazon(storefront)
    results = az.ItemSearch(
        Keywords=keywords,
        SearchIndex=storefront.amazon_category,
        ItemPage=page,
        MinimumPrice=1,
        ResponseGroup='Medium,OfferSummary,Offers,VariationSummary',
    )
    results = fromstring(results)
    Items = results.find(ECS_TAG('Items'))
    item_list = Items.findall(ECS_TAG('Item'))
    asin_list = []
    for item in item_list:
        asin = azasin(item)
        asin_list.append(asin)
        itemkey = '{0}-azlookup-{1}'.format(storefront.site.domain, asin)
        cache.set(itemkey, item, AMAZON_CACHE_TIMEOUT)
    pageskey = '{0}-{1}-azsearch-pages'.format(storefront.site.domain, slugify(keywords))
    try:
        total_pages = int(Items.find(ECS_TAG('TotalPages')).text)
    except AttributeError:
        pass
    else:
        cache.set(pageskey, total_pages, AMAZON_CACHE_TIMEOUT)
    return asin_list


def amazon_search_pages(storefront, keywords):
    key = '{0}-{1}-azsearch-pages'.format(storefront.site.domain, slugify(keywords))
    value = cache.get(key)
    if value is not None:
        return value
    # Cache miss.
    amazon_search(storefront, keywords, 1)
    return cache.get(key)
