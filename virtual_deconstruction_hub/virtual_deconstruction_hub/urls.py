from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.defaults import *
#from search.views import PostSearchView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('',
                    
    # user and authentication URLs
    (r'^myaccount/', include('users.urls')),
    
    # listings URLs
    (r'^listings/', include('listings.urls')),
    
    # survey system URLs
    (r'^survey/', include('survey_system.urls')),
    
    # new listing
    (r'^new/listing$', 'listings.views.create_listing'),
    #delete-verify listing
    (r"^delete-verify", 'listings.views.delete_verify_listing'),
    #edit-verify listing
    (r"^edit-verify", 'listings.views.edit_verify_listing'),
    
    # posts URLs
    (r'^posts/', include('posts.urls')),

    # flagging listings
    (r'^flag/listing/(?P<tag>\w+)/', 'listings.views.flag'),    

    # flagging posts
    (r'^flag/post/(?P<tag>\w+)/', 'posts.views.flag'),
    
    # admin site url
    url(r'^admin/', include(admin.site.urls)),

    #about url
    url(r"^about/", include('statistics_generator.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # search application
    url(r'^search/', 'search.views.search'),    
    
    #set root for static files (css, images, etc)
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    #set root for uploaded photo files
    url(r'^photos/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    # anything else not caught by the above url dispatchers -> home page view (Handles raising 404 errors)
    url(r'^$', 'posts.views.home'),
    

    
    )

