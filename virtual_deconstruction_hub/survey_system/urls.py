from django.conf.urls import patterns, include, url
from django.conf import settings

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('',
                                              
    # survey system urls
    #===========================================================================
    # only need to regex expression for whatever follows /survey/ in url
    # for example domain.com/survey/ directs to this file so you only need to
    # declare a r"successful" in urls below and that will trigger the redirect for 
    # domain.com/survey/successful
    #===========================================================================    
    url(r'^survey', 'survey_system.views.submit_survey'),
    url(r'^survey/successful', 'survey_system.views.successful'),

    )

