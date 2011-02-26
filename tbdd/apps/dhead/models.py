from django.contrib.sites.models import Site
from django.db import models

# Create your models here.


AMAZON_ZONE_CHOICES = (
    ('com', 'United States (com)'),
    ('co.uk', 'United Kingdom (co.uk)'),
    ('de', 'Germany (de)'),
    ('fr', 'France (fr)'),
    ('co.jp', 'Japan (co.jp)'),
    ('ca', 'Canada (ca)'),
)


class Storefront(models.Model):

    site = models.OneToOneField(Site)
    amazon_zone = models.CharField(max_length=10, choices=AMAZON_ZONE_CHOICES)
    amazon_category = models.CharField(max_length=100)
    associate_tag = models.CharField(max_length=100, default='')
    primary_keywords = models.CharField(max_length=255)
    alternate_keywords = models.CharField(max_length=255)
    analytics_footer = models.TextField(blank=True)

    class Meta:
        pass

    def __unicode__(self):
        return u"Storefront for {0}".format(self.site)


class Category(models.Model):

    storefront = models.ForeignKey(Storefront)
    weight = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)

    class Meta:
        ordering = ('-weight', 'title')
        verbose_name_plural = u'Categories'

    def __unicode__(self):
        return u"Category {0}".format(self.title, self.storefront)
