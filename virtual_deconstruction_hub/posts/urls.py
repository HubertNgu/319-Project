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

    # users are emailed an edit-verify post url that directs them here, with query strings for the post id and post uuid
    url(r"^edit-verify$", 'edit_verify_post'),
    # users are directed here when they click the delete button while on an edit-verify page, with query strings for the post id and post uuid
    url(r"^delete-verify/", 'delete_verify_post'),
    # displays the appropriate page for a specific post with a matching url tag if it exists and has been verified
    url(r"^(?P<post_type>[a-zA-Z]{4})/(?P<tag>\w+)", 'posts_specific'),
    # displays the appropriate index page for any of our three types of posts
    url(r"^(?P<post_type>[a-zA-Z]{4})$",'posts_index'),
    )
