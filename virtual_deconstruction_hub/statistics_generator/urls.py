from django.conf.urls import patterns, include, url
from django.conf import settings

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('',
                                              
    #statistics urls
    #===========================================================================
    # only need to regex expression for whatever follows /statistics/ in url
    # for example domain.com/statistics/ directs to this file so you only need to
    # declare a r"current" in urls below and that will trigger the redirect for 
    # domain.com/statistics/current
    #===========================================================================    

    #set root for static files (css, images, etc)
    url(r'^$', 'statistics_generator.views.index'),
    )

