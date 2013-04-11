from django.contrib import admin
from survey_system.models import Survey

class SurveysAdmin(admin.ModelAdmin):
    """Adds a section to the admin backend for working
    with Survey objects in the database. Uses the default
    views provided by Django but makes the display 
    cleaner by ordering fields in columns according to
    list_display. Also adds a search bar for searching
    the search_fields of post objects.
    """
    search_fields = ['item', 'category', 'city', 'comments']
    list_display = ('listing_id','time_submitted','item','category', 'price')
    pass

# Registers this PostsAdmin class with the admin site handler
admin.site.register(Survey, SurveysAdmin)