"""Template tags for tbdd.apps.dhead

All items are given as ElementTree nodes.
"""

from django.template import Library

from tbdd.lib.awsecs import ECS_TAG


register = Library()


@register.filter
def azdetailpageurl(item):
    return item.find(ECS_TAG('DetailPageURL')).text


@register.filter
def azitemattributes(item):
    """Return the ItemAttributes etree element of the item."""
    return item.find(ECS_TAG('ItemAttributes'))


@register.filter
def aztitleattribute(attributes):
    """Return the title of an ItemAttributes."""
    if attributes is None:
        return None
    title = attributes.find(ECS_TAG('Title'))
    if title is None:
        return None
    return title.text


@register.filter
def azfeatureattributes(attributes):
    """Return a list of feature texts of an ItemAttributes."""
    if attributes is None:
        return None
    features = attributes.findall(ECS_TAG('Feature'))
    return [feature.text for feature in features]


@register.filter
def azasin(item):
    return item.find(ECS_TAG('ASIN')).text


@register.filter
def azproductdescription(item):
    reviews = item.find(ECS_TAG('EditorialReviews'))
    if reviews is None:
        return None
    for review in reviews.findall(ECS_TAG('EditorialReview')):
        source = review.find(ECS_TAG('Source')).text
        if source == 'Product Description':
            return review.find(ECS_TAG('Content')).text
    return None


@register.filter
def azformattedprice(item):
    # function item_get_price($item) {
    #   if( count($item->Offers->Offer) > 0 ) $price = $item->Offers->Offer->OfferListing->Price->FormattedPrice;
    #   if( !$price || $price == 'Too low to display') $price = $item->OfferSummary->LowestNewPrice->FormattedPrice;
    #   if( !$price || $price == 'Too low to display') $price = $item->ListedPrice->FormattedPrice;
    #   if( !$price || $price == 'Too low to display') $price = $item->VariationSummary->LowestPrice->FormattedPrice;
    #   if( !$price || $price == 'Too low to display') $price = "N/A";
    #   return $price;
    # }
    price = None
    offers = item.find(ECS_TAG('Offers'))
    if offers is not None:
        offer = offers.find(ECS_TAG('Offer'))
        if offer is not None:
            price = offer.find(ECS_TAG('OfferListing')).find(ECS_TAG('Price')).find(ECS_TAG('FormattedPrice')).text
    if price is None or price == 'Too low to display':
        offersummary = item.find(ECS_TAG('OfferSummary'))
        if offersummary is not None:
            lowestnew = offersummary.find(ECS_TAG('LowestNewPrice'))
            if lowestnew is not None:
                price = lowestnew.find(ECS_TAG('FormattedPrice')).text
    if price is None or price == 'Too low to display':
        listedprice = item.find(ECS_TAG('ListedPrice'))
        if listedprice is not None:
            price = listedprice.find(ECS_TAG('FormattedPrice')).text
    if price is None or price == 'Too low to display':
        variations = item.find(ECS_TAG('VariationSummary'))
        if variations is not None:
            lowestprice = offersummary.find(ECS_TAG('LowestPrice'))
            if lowestprice is not None:
                price = lowestprice.find(ECS_TAG('FormattedPrice')).text
    if price is None or price == 'Too low to display':
        price = 'N/A'
    return price


def _image_dict(image):
    return dict(
        url=image.find(ECS_TAG('URL')).text,
        width=image.find(ECS_TAG('Width')).text,
        height=image.find(ECS_TAG('Height')).text,
    )


@register.filter
def azsmallimage(item):
    """Return the small image URL of an Amazon item."""
    image = item.find(ECS_TAG('SmallImage'))
    if image is None:
        return None
    return _image_dict(image)


@register.filter
def azmediumimage(item):
    """Return the small image URL of an Amazon item."""
    image = item.find(ECS_TAG('MediumImage'))
    if image is None:
        return None
    return _image_dict(image)


@register.filter
def azlargeimage(item):
    """Return the small image URL of an Amazon item."""
    image = item.find(ECS_TAG('LargeImage'))
    if image is None:
        return None
    return _image_dict(image)
