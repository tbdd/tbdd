from json import loads
from xml.etree.ElementTree import fromstring

import bottlenose
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

from tbdd.apps.dhead import cached
from tbdd.apps.dhead.lib import deslugify
from tbdd.apps.dhead.models import Storefront
from tbdd.lib.awsecs import ECS_TAG


def with_request_storefront(fn):
    def wrapped(request, *args, **kwargs):
        site = get_current_site(request)
        if 'storefront' not in kwargs:
            try:
                kwargs['storefront'] = Storefront.objects.get(site=site)
            except Storefront.DoesNotExist:
                kwargs['storefront'] = None
        if kwargs.get('storefront') is not None:
            return fn(request, *args, **kwargs)
        else:
            return HttpResponseNotFound()
    return wrapped


@with_request_storefront
def productdetail(request, keywords=None, title_slug=None, asin=None, template_name="dhead/itemdetail.html", extra_context=None, storefront=None, *args, **kwargs):
    extra_context = extra_context or {}
    keywords = deslugify(keywords)
    item = cached.amazon_lookup(storefront, asin)
    template_context = dict(
        extra_context,
        asin=asin,
        item=item,
        keywords=keywords,
        title_slug=title_slug,
        storefront=storefront,
    )
    return render_to_response(template_name, template_context, RequestContext(request))


@with_request_storefront
def productgo(request, asin=None, extra_context=None, storefront=None, *args, **kwargs):
    pass


@with_request_storefront
def productlist(request, keywords=None, page=1, template_name="dhead/itemlist.html", extra_context=None, storefront=None, *args, **kwargs):
    extra_context = extra_context or {}
    keywords = deslugify(keywords)
    page = int(page)
    # Build search term.
    if keywords is None:
        # Use primary keywords as default search.
        keywords = storefront.primary_keywords
    else:
        # Use search terms in URL if specified.
        keywords = keywords.replace('-', ' ')
    asin_list = cached.amazon_search(storefront, keywords, page)
    item_list = [cached.amazon_lookup(storefront, asin) for asin in asin_list]
    total_pages = cached.amazon_search_pages(storefront, keywords)
    if total_pages is None:
        pages = []
    else:
        pages = range(1, total_pages + 1)
    template_context = dict(
        extra_context,
        keywords=keywords,
        item_list=item_list,
        pages=pages,
        storefront=storefront,
    )
    return render_to_response(template_name, template_context, RequestContext(request))


@with_request_storefront
def about(request, template_name="dhead/about.html", extra_context=None, storefront=None, *args, **kwargs):
    extra_context = extra_context or {}
    template_context = dict(
        extra_context,
        storefront=storefront,
    )
    return render_to_response(template_name, template_context, RequestContext(request))


@with_request_storefront
def privacy(request, template_name="dhead/privacy.html", extra_context=None, storefront=None, *args, **kwargs):
    extra_context = extra_context or {}
    template_context = dict(
        extra_context,
        storefront=storefront,
    )
    return render_to_response(template_name, template_context, RequestContext(request))
