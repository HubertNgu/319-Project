from django.conf.urls import patterns, url

# ORDER MATTERS!! Django will direct to first match it encounters, so make sure the most generic url regex is the lowest in the list
urlpatterns = patterns('posts.views',
                                              
    #posts urls
    #===========================================================================
    # only need to regex expression for whatever follows /posts/ in url
    # for example domain.com/posts/ directs to this file so you only need to
    # declare a r"(?P<post_type>[a-z]{4})/new" in urls below and that will trigger the redirect for 
    # domain.com/posts/xxxx/new
    #===========================================================================    

    # looks for url patter domain.com/posts/4CHARTYPESTRING/new, calls posts.views.create_post(request, post_type='4CHARTYPESTRING')
    url(r"(?P<post_type>[a-zA-Z]{4})/new", 'new_post'),
    url(r"edit-verify", 'edit_verify_post'),
    #url(r"(?P<post_type>[a-zA-Z]{4})/search", 'search_posts'),
    # displys the appropriate index page for any of our three types of posts
    url(r"(?P<post_type>[a-zA-Z]{4})/(?P<tag>\w+)", 'posts_specific'),
    url(r"(?P<post_type>[a-zA-Z]{4})",'posts_index'),
    )

