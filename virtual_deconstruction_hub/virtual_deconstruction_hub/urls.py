from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    # Examples:
    # url(r'^$', 'virtual_deconstruction_hub.views.home', name='home'),
    # url(r'^virtual_deconstruction_hub/', include('virtual_deconstruction_hub.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^test/', include(admin.site.))
    url(r"listings", 'direct_to_template', {"template": "listings/listings_index.html"}),
    url(r"blog", 'direct_to_template', {"template": "posts/blog_index.html"}),
    url(r"about", 'direct_to_template', {"template": "about.html"}),
    url(r"^$", 'direct_to_template', {"template": "base.html"})
    )
