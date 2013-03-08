from django.contrib import admin
from listings.models import Listing

class ListingsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['creator']}),
        (None,               {'fields': ['textContent']})
        ,
    ]
    list_display = ('title', 'created', 'creator')
    list_filter = ['created']
    search_fields = ['title']

admin.site.register(Listing, ListingsAdmin)