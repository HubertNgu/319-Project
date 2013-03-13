from django.conf.urls import patterns, include, url
from django.conf import settings

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('',
                                              
    #posts urls
    #===========================================================================
    # only need to regex expression for whatever follows /posts/ in url
    # for example domain.com/posts/ directs to this file so you only need to
    # declare a r"(?P<post_type>[a-z]{4})/new" in urls below and that will trigger the redirect for 
    # domain.com/posts/xxxx/new
    #===========================================================================    

    #url(r"blog", 'direct_to_template', {"template": "posts/blogs_index.html"}),
    url(r"project_ideas", 'direct_to_template', {"template": "posts/projects_index.html"}),
    url(r"user_stories", 'direct_to_template', {"template": "posts/stories_index.html"}),
    # looks for url patter domain.com/posts/4CHARTYPESTRING/new, calls posts.views.create_post(request, post_type='4CHARTYPESTRING')
    url(r"(?P<post_type>[a-z]{4})/new", 'posts.views.new_post'),
    url(r"(?P<post_type>[a-z]{4})/verification", 'posts.views.verify_post'),

    )

