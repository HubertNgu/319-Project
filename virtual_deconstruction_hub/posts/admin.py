from django.contrib import admin
from posts.models import Post

class PostsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostsAdmin)