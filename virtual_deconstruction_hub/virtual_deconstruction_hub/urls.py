from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('django.views.generic.simple',
    # Examples:
    # url(r'^$', 'virtual_deconstruction_hub.views.home', name='home'),
    # url(r'^virtual_deconstruction_hub/', include('virtual_deconstruction_hub.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^test/', include(admin.site.))
    url(r"blog", 'direct_to_template', {"template": "posts/posts_index.html"}),
    url(r"about", 'direct_to_template', {"template": "about.html"}),
    
    # listings URLs
    url(r"listings/new", 'direct_to_template', {"template": "listings/listings_new.html"}),
    url(r"listings", 'direct_to_template', {"template": "listings/listings_index.html"}),
    url(r"^$", 'direct_to_template', {"template": "base.html"})
    )
