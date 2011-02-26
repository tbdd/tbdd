from django.contrib import admin

from tbdd.apps.dhead.models import Category, Storefront


class CategoryInline(admin.TabularInline):

    model = Category


class StorefrontAdmin(admin.ModelAdmin):

    list_display = ('site', 'primary_keywords')
    inlines = [
        CategoryInline,
    ]


admin.site.register(Storefront, StorefrontAdmin)
