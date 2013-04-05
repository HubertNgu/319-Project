from django.contrib import admin
from posts.models import Post

class PostsAdmin(admin.ModelAdmin):
    """Adds a section to the admin backend for working
    with Post objects in the database. Uses the default
    views provided by Django but makes the display 
    cleaner by ordering fields in columns according to
    list_display. Also adds a search bar for searching
    the search_fields of post objects.
    """
    search_fields = ['title', 'creator', 'url', 'text_content']
    list_display = ('title','creator','created','last_modified', 'type','url','flag_count','verified')
    pass

# Registers this PostsAdmin class with the admin site handler
admin.site.register(Post, PostsAdmin)