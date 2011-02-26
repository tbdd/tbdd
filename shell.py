import bottlenose
from xml.etree.ElementTree import fromstring

from django.conf import settings

ECS_TAG = '{{http://webservices.amazon.com/AWSECommerceService/2009-10-01}}{0}'.format

def amazon(associate_tag):
    return bottlenose.Amazon(settings.ACCESS_KEY_ID, settings.SECRET_ACCESS_KEY, associate_tag)

print 'Now use az = amazon(associate_tag)'
