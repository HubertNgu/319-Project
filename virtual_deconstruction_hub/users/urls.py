from django.conf.urls import patterns, include, url
from django.conf import settings

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('',
                                              
    # user and authentication urls
    
    #===========================================================================
    # only need to regex expression for whatever follows /users/ in url
    # for example domain.com/listings/ directs to this file so you only need to
    # declare a r"signup" in urls below and that will trigger the redirect for 
    # domain.com/users/signup
    #===========================================================================
    url(r'^login', 'users.views.index'),
    url(r'^signup', 'users.views.signup'),
    url(r'^logout', 'users.views.logout_user'),
    url(r'^profile', 'users.views.myaccount'),
    url(r'^listings', 'users.views.listings'),
    url(r'^editaccount', 'users.views.editaccount'),
    url(r'^verification', 'users.views.verification'),
    url(r'^verifyfail', 'users.views.verifyfail'),
    url(r'^verifyemail/$', 'users.views.verifyemail'),
    url(r'^(?P<post_type>[a-zA-Z]{4})','users.views.posts'),
    url(r'', 'users.views.index'),

    #set root for static files (css, images, etc)
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

