from django.conf.urls import patterns, include, url
from django.conf import settings

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('',
                                              
    # profile URLs
    #===========================================================================
    # only need to regex expression for whatever follows /profiles/ in url
    # for example domain.com/profiles/ directs to this file so you only need to
    # declare a r"(p<profile_id>\d)" in urls below and that will trigger the redirect for 
    # domain.com/profiles/xxxxx
    #===========================================================================

    )

