from django.contrib import admin
from listings.models import Listing

class ListingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Listing, ListingsAdmin)