from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('',

    # user and authentication URLs
    (r'^users/', include('users.urls')),
    
    # listings URLs
    (r'listings/', include('listings.urls')),
    
    # survey system URLs
    (r'^survey/', include('survey_system.urls')),
    
    # posts URLs
    (r'posts/', include('posts.urls')),
    
    # profile URLs
    (r'profiles/', include('userprofile.urls')),
    
    #statistics urls
    (r'statistics/', include('statistics_generator.urls')),

    # admin site url
    url(r'^admin/', include(admin.site.urls)),

    #about url
    url(r"about", 'direct_to_template', {"template": "about.html"}),

    # root url - home page
    url(r"^$", include('statistics_generator.urls')),
    
    # Examples:
    # url(r'^$', 'virtual_deconstruction_hub.views.home', name='home'),
    # url(r'^virtual_deconstruction_hub/', include('virtual_deconstruction_hub.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #set root for static files (css, images, etc)
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    
    )

