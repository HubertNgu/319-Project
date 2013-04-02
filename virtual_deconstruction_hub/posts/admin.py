from django.contrib import admin
from posts.models import Post

class PostsAdmin(admin.ModelAdmin):
    """Adds a section to the admin backend for working
    with Post objects in the database. Uses the default
    views provided by Django
    """
    pass

# Registers this PostsAdmin class with the admin site handler
admin.site.register(Post, PostsAdmin)