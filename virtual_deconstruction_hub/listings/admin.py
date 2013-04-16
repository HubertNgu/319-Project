from django.contrib import admin
from listings.models import Listing
from listings.models import Photo


class PhotoInline(admin.TabularInline):
    model = Photo

class ListingsAdmin(admin.ModelAdmin):
    """Adds a section to the admin backend for working
    with Listing objects in the database. Uses the default
    views provided by Django but makes the display 
    cleaner by ordering fields in columns according to
    list_display. Also adds a search bar for searching
    the search_fields of post objects.
    """
    search_fields = ['title', 'creator', 'url', 'text_content', 'city', 'address']
    list_display = ( 'title','creator','created', 'expires','last_modified', 'for_sale','category','city','url','flag_count','expired','verified')
    inlines = [PhotoInline,]
    pass

admin.site.register(Listing, ListingsAdmin)