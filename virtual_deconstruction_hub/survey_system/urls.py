from django.conf.urls import patterns, include, url
from django.conf import settings

UUID_REGEX = '(?P<survey_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})'

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('survey_system.views',
                                              
    # survey system urls
    #===========================================================================
    # only need to regex expression for whatever follows /survey/ in url
    # for example domain.com/survey/ directs to this file so you only need to
    # declare a r"successful" in urls below and that will trigger the redirect for 
    # domain.com/survey/successful
    #===========================================================================    
    url(r'^successful/%s$' % UUID_REGEX, 'survey'),
    url(r'^expired/%s$' % UUID_REGEX, 'survey'),
    url(r'^%s$' % UUID_REGEX, 
        'survey'),
   ) 
