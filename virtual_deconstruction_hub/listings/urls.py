from django.conf.urls import patterns, include, url
from django.conf import settings

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('',
                                              
    # listings URLs
    #===========================================================================
    # only need to regex expression for whatever follows /listings/ in url
    # for example domain.com/listings/ directs to this file so you only need to
    # declare a r"new" in urls below and that will trigger the redirect for 
    # domain.com/listings/new
    #===========================================================================    
    url(r"new", 'direct_to_template', {"template": "listings/listings_new.html"}),
    url(r"^$", 'direct_to_template', {"template": "listings/listings_index.html"}),

    )
