from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('django.views.generic.simple',
    #url(r'^$','virtual_deconstruction_hub.views.index'),
    url(r'^users/login', 'users.views.index'),
    url(r'^users/signup', 'users.views.signup'),
    url(r'^users/logout', 'users.views.logout_user'),
    url(r'^users/myaccount', 'users.views.myaccount'),
    # Examples:
    # url(r'^$', 'virtual_deconstruction_hub.views.home', name='home'),
    # url(r'^virtual_deconstruction_hub/', include('virtual_deconstruction_hub.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^test/', include(admin.site.))

    # user and authentication urls
    url(r"login", "direct_to_template", {"template": "authentication/login.html"}),
    
    #posts urls
    url(r"blog", 'direct_to_template', {"template": "posts/blogs_index.html"}),
    url(r"project_ideas", 'direct_to_template', {"template": "posts/projects_index.html"}),
    url(r"user_stories", 'direct_to_template', {"template": "posts/stories_index.html"}),
    
    #about url
    url(r"about", 'direct_to_template', {"template": "about.html"}),
    
    # listings URLs
    url(r"listings/new", 'direct_to_template', {"template": "listings/listings_new.html"}),
    url(r"listings", 'direct_to_template', {"template": "listings/listings_index.html"}),
    
    # root url - home page
    url(r"^$", 'direct_to_template', {"template": "statistics/statistics_main.html"}),
    
    #set root for static files (css, images, etc)
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

