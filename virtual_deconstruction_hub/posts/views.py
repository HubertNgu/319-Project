# Create your views here.
from django.http import HttpRequest
from django.http import Http404
from django.shortcuts import render_to_response
#from django.template.defaulttags import csrf_token
from django.template import RequestContext
#from django.contrib.auth.models import User
from posts.models import *
from listings.models import Listing
#from django.contrib.auth import authenticate,login,get_user
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
import re
import string
import random
from mailer.views import send_post_verification_email
from django.contrib.sites.models import Site
import logging
from util import constants

logger = logging.getLogger(__name__)

#PAGE_SIZE = int(constants.posts_results_page_size)
#DB_RESULTS_MAX = int(constants.db_max_results)
PAGE_SIZE = int(settings.POSTS_PAGE_SIZE)
DB_RESULTS_MAX = int(settings.DB_RESULTS_MAX)

# Dictionary of pairings for relative template paths. Every rendering of a template for a post object references it's specific key and uses the associated
# template path from this dictionary. For example, the index view is type dependent and will user the template associated with "proj_list" key if asked 
# for the Project Ideas index page. Currently all the different types use the same template for their index and individual pages, however this dictionary
# provides a single point for making template changes without having to edit any other section of code in this file.  
TEMPLATE_PATHS = {'proj_list': 'posts/posts_list.html', 'blog_list': 'posts/posts_list.html', 'stry_list': 'posts/posts_list.html',
                  'proj_single': 'posts/posts_single.html', 'blog_single': 'posts/posts_single.html', 'stry_single': 'posts/posts_single.html',
                  'posts_new': 'posts/posts_new.html',
                  'posts_delete': 'posts/posts_delete.html',
                  'posts_edit': 'posts/posts_edit.html',
                  'posts_success':'posts/new_post_success.html',
                  'posts_upload': 'uploadfile/upload.html',
                  }
# Dictionary of pairings for url paths. Every redirect needed references it's specific key and uses the associated url path from this dictionary.
# For example, when generating an edit-verify link to email a user after they have created a post, that method gets the value associated with the 
# 'posts_edit-verify' key and uses it to build the url. In this way the dictionary below provides a single point for making url changes without
# having to edit any other section of code in this file. 
URL_PATHS = {'posts_edit-verify': '/posts/edit-verify',
             'posts_delete-verify': '/posts/delete-verify/',
             'posts_root': '/posts/',
             'blog_new': '/posts/new/blog',
             'proj_new': '/posts/new/proj',
             'stry_new': '/posts/new/stry'}

# Dictionary of pairings for post page titles. Every form render for post creation/edits references it's specific key and uses the associated title
# from this dictionary to insert into the template text.
# For example, when a user clicks to create a new Success Story post, when the post creation form is rendered and additional argument is passed that 
# references the value for the 'stry' key and the user will see "Create a new success stories post:" above the form.
# In this way the dictionary below provides a single point for making small title changes without having to edit any other section of code in this file. 
POST_TYPE_TITLES = {'blog': "Blog", 'proj': "Project Ideas", "stry": "Success Stories", 'upload': "Upload"}

# Dictionary of pairings for post page messages that are optionally passed to a template when rendered. Instead of hard coding separate messages every time,
# they are referenced by a specific key and the associated message is passed from this dictionary to insert into the template when needed.
# For example, when a user submits a new post, if the post creation form valid they are redirected to a success page with the message associated with
# the 'verified_post' key displayed.
# In this way the dictionary below provides a single point for making message changes without having to edit any other section of code in this file. 
MESSAGES = {'verified_post': "Your post has been verified and will be displayed on the site. You can make changes to your post here if you wish.",
            'edit_success': "Your changes have been saved. You can make further changes to your post if you wish."}

def new_post(request, post_type):
    """View for creating a new post of any of the three types.
    This view renders a PostForm for the user to fill out and submit
    when called with an HTTP GET request. If called with an HTTP POST
    request, this view will validate the form data and if it is valid,
    will process further:
        -If user has a registered account and is logged in, will mark
        post as verified, save the post object to the database and
        redirect the user to their newly created post url.
        -If user is not registered or logged in, will mark post as
        unverified, save the post object to the database, generate
        a post edit/verification link and email it to the email
        address provided by the user.
    This view also handles photo uploads for a post.
    
    Arguments:
    
    request -- the HTTP request from the users browser
    post_type -- the type of the posts to be retrieved form the database
    """
    # Check for logged in user and set template parameters accordingly
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
        # only registered users are allowed to create posts, if not register render non valid user page
        return render_to_response("users/not_user.html", {'logparams': logparams}, context_instance=RequestContext(request))    
    if post_type == "blog" and request.user.is_superuser == False:
        # only super users (site admins) are allowed to create blog posts, if not register render non valid admin page
        return render_to_response("users/not_admin.html", {'logparams': logparams}, context_instance=RequestContext(request))
    
    # format the post_type that was in the URL to lowercase string
    post_type = str(post_type.lower())
    pictureform = UploadForm()
    #action for submit button
    submit_action = URL_PATHS.get(post_type+'_new')
    
    # Generate and render a fresh post creation form on HTTP GET requests.
    if request.method == 'GET':
        # setup the post creation form and initialize creator fields and email verification fields
        # (email verification left here so that it will be a simple matter to open non blog post creation to 
        # unregistered users if desired.
        form = PostForm(instance=Post(), initial={'creator':request.user.email, 'email_verification':request.user.email})
        if request.user.is_authenticated():
            form.fields['creator'].widget = forms.HiddenInput()
            form.fields['email_verification'].widget = forms.HiddenInput()
           
        
        form_args = {'form':form, 'submit_action':submit_action, 'message':None, 
                     'post_type_title':POST_TYPE_TITLES.get(post_type), 
                     'pictureform':pictureform, 'logparams': logparams}
        # render the form for the user to fill out and submit
        return render_to_response(TEMPLATE_PATHS.get("posts_new"), form_args, context_instance=RequestContext(request))
    
    # Validate a post creation form on HTTP POST requests and render appropriate response
    if request.method == 'POST':
        # get the completed form from the request and process
        post_form = PostForm(request.POST)
        if request.user.is_authenticated():
            post_form.fields['creator'].widget = forms.HiddenInput()
            post_form.fields['email_verification'].widget = forms.HiddenInput()
        
        if post_form.is_valid() and request.POST.get("notnewpost") == None:
            # generate values for non-user defined fields in post object,
            # write to db and return post object
            post = post_form.save(commit=False)
            post.set_type(post_type.lower())
            post.set_url( tag_maker("_", post) )
            post_url = post.get_url()
            post_url = HttpRequest.build_absolute_uri(request, post_url)
            if request.user.is_authenticated():
                post.verified = True
            post.save()
            postid = post.id
        
        form = UploadForm(request.POST, request.FILES)
        if request.POST.get("notnewpost") != None:
            postid = request.POST.get("postid")
            post = Post.objects.get(id = postid )
            #post.set_type(post_type.lower())
            #post.set_url( tag_maker("_", post) )
            post_url = post.get_url()
        form_args = {'form':post_form, 'submit_action':submit_action, 'post_url' : post_url, 'post':post, 'logparams':logparams}
        if form.is_valid():
            form_args = {'post':post, 'post_url': post_url, 'logparams':logparams}
            photo = Photo(photo = request.FILES['picture'], post = post, caption = request.POST.get('caption') )
            photo.save()            
            if request.POST.get('pictureform') == "1" and request.POST.get("issubmit") != "1":
                #photolist = Photo.objects.filter(post_id = post.id)
                addanotherprevious = list()
                for o in Photo.objects.filter(post_id = post.id):
                    item = [o.photo.name,o.id] 
                    addanotherprevious.append(item)
            
                form_args = {'form':post_form, 'submit_action':submit_action, 
                              'pictureform': pictureform,
                             'postid' :postid, 'addanotherprevious' : addanotherprevious, 'logparams':logparams}
                return render_to_response("posts/posts_new.html", form_args, context_instance=RequestContext(request))
            
        #====================================================================
        # Testing - REMOVE LATER - this just creates x # of posts of a given
        # type whenever a single one is created from the web, just used to 
        # populate db for testing purposes
        #====================================================================
        #multiple_entries_for_testing(10000)

        if post.is_verified():
            # if post is already verified, redirect user to their newly created post
            return redirect("/posts/" + post_type +"/" + post.url, context_instance=RequestContext(request))

        # create a verification/edit link and send with mailer then direct to success message page
        user_email = post.get_creator()
        verify_url = '%s/posts/%s?post_id=%s&uuid=%s' % (Site.objects.get_current(), URL_PATHS.get('posts_edit-verify'), post.id, post.get_uuid())
        send_post_verification_email(verify_url, user_email, post_type)
        return render_to_response(TEMPLATE_PATHS.get("posts_success"), form_args, context_instance=RequestContext(request))
    else:
      
        # if form submission not valid, redirect back to form with error messages
        form_args = {'form':post_form, 'submit_action':submit_action, 'message':None, 'post_type_title':POST_TYPE_TITLES.get(post_type), 'pictureform': pictureform, 'post_type': post_type}
        return render_to_response(TEMPLATE_PATHS.get("posts_new"), form_args, context_instance=RequestContext(request))

    raise Http404
def edit_verify_post(request):
    """View that users are directed to when they click the edit/verification
    link emailed to them after creating a post as an anonymous user.
    This view validates the verification link for the post and then marks it
    as verified if it was not already. This will allow it to be shown on the
    site. This view also allows the user to edit their post if desired.

    Arguments:
    
    request -- the HTTP request from the users browser
    """
    # Check for logged in user and set template parameters accordingly
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext] 
    post_id = request.GET.get('post_id')
    uuid = request.GET.get('uuid')
    #action for submit button
    submit_action = URL_PATHS.get('posts_edit-verify') + '?post_id=' + post_id + '&uuid=' + uuid
    post_url = None
    message = None
    # try to get the specified post from the database,
    # raise 404 error if not found.
    post = get_object_or_404(Post, id=str(post_id))
   
    pictureform = UploadForm()
    listpictures =list()
    listdeleteid = list()
    if(request.POST.get("deletephoto") != None and request.POST.get("deletephotoyes") == "true" ):
        deletephoto = Photo.objects.get(id = request.POST.get("deletephoto"))
        deletephoto.delete() 

    if request.method == 'GET':     
        # if post hasn't been verified yet and the id and uuid
        # in the url query string are correct, mark as verified
        # set verified message and redirect to post edit form. 
        if not post.is_verified():   
            if post and (post.get_uuid() == str(uuid)):
                 post.mark_verified()
                 post.save()
                 message = MESSAGES.get('verified_post')
            else:
                # the post_id and uuid provided do not match anything in db correctly
                # so redirect to 404 as this page doesn't exist for this combination
                raise Http404
        #post verified by this point, render edit page with edit form and message
        edit_form = EditPostForm(instance=post)
        try:
            for o in Photo.objects.filter(post_id = post_id):
                item = [o.photo.name,o.id]
                listpictures.append(item)
                   
        except:
            listpictures = None
            listdeleteid = None
        delete_button = URL_PATHS.get('posts_delete-verify') + '?post_id=' + str(post.id) + '&uuid=' + uuid
        form_args = {'form':edit_form, 'message': message, 'submit_action': submit_action, 'post_type_title':POST_TYPE_TITLES.get(post.get_type()), 'logparams': logparams, 
                     'post_type': post.get_type(), 'delete_button': delete_button, 'listpictures':listpictures, 'pictureform' : pictureform,'listdeleteid' :listdeleteid}
        return render_to_response(TEMPLATE_PATHS.get("posts_edit"), form_args, context_instance=RequestContext(request))
        
    if request.method == 'POST':
        edit_form = EditPostForm(request.POST, instance=post)
        form = UploadForm(request.POST, request.FILES)
       
        #if post_form valid, process new post
        delete_button = URL_PATHS.get('posts_delete-verify') + '?post_id='  + str(post.id) + '&uuid=' + uuid
        if edit_form.is_valid():
            post_url = HttpRequest.build_absolute_uri(request, edit_form.cleaned_data.get('url'))
            edit_form.save()
            if form.is_valid():
                photo = Photo(photo = request.FILES['picture'], post = post )
                photo.save()  
            #if user wants to add another picture        
            if request.POST.get('pictureform') == "1" and request.POST.get("issubmit") != 1:
                photolist = Photo.objects.filter(post_id = post.id)
                addanotherprevious = list()
                #get all the names of the previously added pictures
            # This redirects back to edit form with edit success message
            try:
                for o in Photo.objects.filter(post_id = post_id):
                    item = [o.photo.name,o.id]
                    listpictures.append(item)
                   
            except:
                listpictures = None
                listdeleteid = None
            form_args = {'form':edit_form, 'submit_action':submit_action, 
                         'message':MESSAGES.get('edit_success'),
                          'post_type_title':POST_TYPE_TITLES.get(post.get_type()), 
                          'post_url': post_url, 'post_type': post.get_type(),
                           'logparams' : logparams, 
                           'delete_button': delete_button,
                           'listpictures':listpictures,
                           'pictureform' : pictureform,
                           'listdeleteid': listdeleteid}
            return render_to_response(TEMPLATE_PATHS.get("posts_edit"), form_args, 
                                      context_instance=RequestContext(request))
        else:
            # if form submission not valid, redirect back to edit form with error messages
            form_args = {'form':edit_form, 'submit_action':submit_action, 'message':None, 'post_type_title':POST_TYPE_TITLES.get(post.get_type()), 'post_type': post.get_type(),  'logparams':logparams, 'delete_button': delete_button,
                           'listpictures':listpictures}
            return render_to_response(TEMPLATE_PATHS.get("posts_edit"), form_args, context_instance=RequestContext(request))   
        raise Http404
def posts_index(request, post_type):
    """View that renders an index page for a specified post type.
    This view queries the database for posts with a matching type,
    paginates the results and passes the objects to a template to 
    be rendered for display. If a 'page' query string is present
    in url, the results rendered will go to the specified page #.

    Arguments:
    
    request -- the HTTP request from the users browser
    post_type -- the type of the posts to be retrieved form the database
    """
    # Check for logged in user and set template parameters accordingly
    loggedin = None
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
        loggedin = "yes"
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    username = None
    postname = None
    if request.user.is_superuser == True:
        username = request.user.username
    if(post_type == "blog" and username == None) or loggedin == None:
        loggedin = None
    if post_type == "blog":
        postname = "blog"
    if post_type == "proj":
        postname = 'project idea'
    if post_type == "stry":
        postname = "success story"
    # format the post_type that was in the URL to lowercase string
    post_type = str(post_type.lower())
    # build database query for index page results. Only return posts with the specified type
    # that have been verified and order by created from newest to oldest.
    query = Post.objects.filter(type=post_type).filter(verified=True).order_by('-created')[:DB_RESULTS_MAX]
    # paginate the results and if page paramter provided, set to that page
    paginator = Paginator(query , PAGE_SIZE)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts= paginator.page(paginator.num_pages)
    form_args = {'posts':posts, 'message': None, 'post_type_title':postname, 
                 'post_type': post_type, 'logparams': logparams, 'username': username, 'loggedin':loggedin}
    return render_to_response(TEMPLATE_PATHS.get(post_type+'_list'),form_args, context_instance=RequestContext(request))
    raise Http404        
def posts_specific(request, post_type, tag):
    """View that renders a page for displaying a specific post.
    This view queries the database for post with a matching tag
    and if it exists passes the post object to a template and 
    renders it for display. If object is not found a 404 error
    is raised.

    Arguments:
     
    request -- the HTTP request from the users browser
    tag -- the url tag of the post to be displayed
    """
    # Check for logged in user and set template parameters accordingly
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    # format the post_type that was in the URL to lowercase string
    post_type = str(post_type.lower())
    # format the post tag that was provided in the URL to lowercase string
    tag.lower()
    if request.method == 'GET':
        # query the database for a post with that url
        # return 404 if not found or if found but not verified
        # otherwise render the single post template with the post object
        query = get_object_or_404(Post, url=tag)
        if query.is_verified():
            form_args = {'post':query, 'message':None, 'post_type_title':POST_TYPE_TITLES.get(post_type), 'post_type': post_type, 'logparams' : logparams}
            return render_to_response( TEMPLATE_PATHS.get(post_type+"_single"),form_args, context_instance=RequestContext(request))
        else:
            raise Http404()   
        
def delete_verify_post(request):
    """View that users are directed to when they click to delete a post.
    This view validates the deletion link for the post and then marks it
    as unverified. This will prevent it from showing on the site but will
    allow the user to 'undelete' it if they want to later and also allows
    the site to retain content posted to the system.

    Arguments:
    
    request -- the HTTP request from the users browser
    """
    #  only accepts HTTP POST requests 
    if request.method == 'POST':  
        #grab the post id and uuid from url query string
        post_id = request.GET.get('post_id')
        uuid = request.GET.get('uuid')
        # try and grab the post from the database, if no found raise 404 error
        post = get_object_or_404(Post, id=str(post_id))
        # Mark post as unverified and save. This can be easily modified
        # to delete posts if that is desired by calling post.delete() instead.
        post.verified = False
        post.save()
        message = "Your post will no longer be displayed."
        form_args = { "message" : message, }
        # renders a delete successful view with success message
        return render_to_response(TEMPLATE_PATHS.get("posts_delete"), form_args, context_instance=RequestContext(request))
    else:
        raise Http404
    
def home(request):
    """View for the home page at the root url www.domain.com/
    This view fetched the latest blog post from the database and displays it
    at the top of the page as a featured post. It also fetches the 5 most recent
    listings to be displayed underneath the featured blog post.
    
    Arguments:
    
    request -- the HTTP request from the users browser
    """
    # only accepts HTTP GET requests
    if request.method == 'GET':  
        # Check for logged in user and set template parameters accordingly
        if request.user.is_authenticated():
            logtext = "Logout"
            accounttext = "My Account"
            welcometext = request.user.username
            logparams=[logtext,accounttext, welcometext]
        else: 
            logtext = "Login"
            accounttext = "Sign Up"
            logparams=[logtext,accounttext]
        
        #Try to fetch latest blog object from database, if there isn't one, set to none
        try:
            latest_blog = Post.objects.filter(type='blog').filter(verified=True).latest('created')
        except:
            latest_blog = None
        #Try to fetch one photo for the latest blog object, if there isn't one, set to none
        try:
            blog_photo = latest_blog.photo_set.all()
            blog_photo = blog_photo[0]
        except:
            blog_photo = None
        #Try to fetch latest listings objects from database, if there aren't any, set to none
        try:
            listings = Listing.objects.filter(verified=True, expired=False).order_by('-last_modified')[:5]
        except:
            listings = None
        
        # render response form with form_args list of parameters  
        form_args = {'post': latest_blog, 'listings': listings, 'logparams': logparams, 'blog_photo': blog_photo}
        return render_to_response('posts/home_page.html', form_args, context_instance=RequestContext(request))
    else: raise Http404

                                                                                                        
    
        

def tag_maker(space_replacement_char, post):
    """ Takes in a post and removes any no a-z,A-Z,0-9 characters in the title,
     replaces all spaces with the given Space_replacement_char then returns a
     unique string in all lowercase to use as the relative url
     
     Arguments:
     space_replacement_char -- an ASCII character that will replace all space characters
     post - a post object to generate the tag for
    """
    tag = re.sub(r'\W+', '', post.get_title().lower().replace (" ", space_replacement_char ))
    #check that url is unique in db, if url already exists
    # append a random 10 char string to the end
    if Post.objects.filter(url=tag).count() > 0:
        tag = tag + space_replacement_char + random_string_generator(10)
    return tag

def random_string_generator(size, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    """ Generate a random string of the specified size using ASCII lower and upper case characters
    and digits 0-9
     
     Arguments:
     size -- an integer specifying the desired length of the random string to be generated
    """
    return ''.join(random.choice(chars) for x in range(size))


def multiple_entries_for_testing(number):
    ## fill in test data in db: writes 100 post objects of same type as whatever new form you are entering
    email = 'seanslipetz@gmail.com'
    title = ' of ' + str(number) + 'test postings'
    content = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Nam cursus. Morbi ut mi. Nullam enim leo, egestas id, condimentum at, laoreet mattis, massa. Sed eleifend nonummy diam. Praesent mauris ante, elementum et, bibendum at, posuere sit amet, nibh. Duis tincidunt lectus quis dui viverra vestibulum. Suspendisse vulputate aliquam dui. Nulla elementum dui ut augue. Aliquam vehicula mi at mauris. Maecenas placerat, nisl at consequat rhoncus, sem nunc gravida justo, quis eleifend arcu velit quis lacus. Morbi magna magna, tincidunt a, mattis non, imperdiet vitae, tellus. Sed odio est, auctor ac, sollicitudin in, consequat vitae, orci. Fusce id felis. Vivamus sollicitudin metus eget eros.
Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In posuere felis nec tortor. Pellentesque faucibus. Ut accumsan ultricies elit. Maecenas at justo id velit placerat molestie. Donec dictum lectus non odio. Cras a ante vitae enim iaculis aliquam. Mauris nunc quam, venenatis nec, euismod sit amet, egestas placerat, est. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Cras id elit. Integer quis urna. Ut ante enim, dapibus malesuada, fringilla eu, condimentum quis, tellus. Aenean porttitor eros vel dolor. Donec convallis pede venenatis nibh. Duis quam. Nam eget lacus. Aliquam erat volutpat. Quisque dignissim congue leo.
Mauris vel lacus vitae felis vestibulum volutpat. Etiam est nunc, venenatis in, tristique eu, imperdiet ac, nisl. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In iaculis facilisis massa. Etiam eu urna. Sed porta. Suspendisse quam leo, molestie sed, luctus quis, feugiat in, pede. Fusce tellus. Sed metus augue, convallis et, vehicula ut, pulvinar eu, ante. Integer orci tellus, tristique vitae, consequat nec, porta vel, lectus. Nulla sit amet diam. Duis non nunc. Nulla rhoncus dictum metus. Curabitur tristique mi condimentum orci. Phasellus pellentesque aliquam enim. Proin dui lectus, cursus eu, mattis laoreet, viverra sit amet, quam. Curabitur vel dolor ultrices ipsum dictum tristique. Praesent vitae lacus. Ut velit enim, vestibulum non, fermentum nec, hendrerit quis, leo. Pellentesque rutrum malesuada neque.
Nunc tempus felis vitae urna. Vivamus porttitor, neque at volutpat rutrum, purus nisi eleifend libero, a tempus libero lectus feugiat felis. Morbi diam mauris, viverra in, gravida eu, mattis in, ante. Morbi eget arcu. Morbi porta, libero id ullamcorper nonummy, nibh ligula pulvinar metus, eget consectetuer augue nisi quis lacus. Ut ac mi quis lacus mollis aliquam. Curabitur iaculis tempus eros. Curabitur vel mi sit amet magna malesuada ultrices. Ut nisi erat, fermentum vel, congue id, euismod in, elit. Fusce ultricies, orci ac feugiat suscipit, leo massa sodales velit, et scelerisque mi tortor at ipsum. Proin orci odio, commodo ac, gravida non, tristique vel, tellus. Pellentesque nibh libero, ultricies eu, sagittis non, mollis sed, justo. Praesent metus ipsum, pulvinar pulvinar, porta id, fringilla at, est.
Phasellus felis dolor, scelerisque a, tempus eget, lobortis id, libero. Donec scelerisque leo ac risus. Praesent sit amet est. In dictum, dolor eu dictum porttitor, enim felis viverra mi, eget luctus massa purus quis odio. Etiam nulla massa, pharetra facilisis, volutpat in, imperdiet sit amet, sem. Aliquam nec erat at purus cursus interdum. Vestibulum ligula augue, bibendum accumsan, vestibulum ut, commodo a, mi. Morbi ornare gravida elit. Integer congue, augue et malesuada iaculis, ipsum dui aliquet felis, at cursus magna nisl nec elit. Donec iaculis diam a nisi accumsan viverra. Duis sed tellus et tortor vestibulum gravida. Praesent elementum elit at tellus. Curabitur metus ipsum, luctus eu, malesuada ut, tincidunt sed, diam. Donec quis mi sed magna hendrerit accumsan. Suspendisse risus nibh, ultricies eu, volutpat non, condimentum hendrerit, augue. Etiam eleifend, metus vitae adipiscing semper, mauris ipsum iaculis elit, congue gravida elit mi egestas orci. Curabitur pede.
Maecenas aliquet velit vel turpis. Mauris neque metus, malesuada nec, ultricies sit amet, porttitor mattis, enim. In massa libero, interdum nec, interdum vel, blandit sed, nulla. In ullamcorper, est eget tempor cursus, neque mi consectetuer mi, a ultricies massa est sed nisl. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Proin nulla arcu, nonummy luctus, dictum eget, fermentum et, lorem. Nunc porta convallis pede."""
    for i in xrange(0,number):
        ver=True
        post_type='blog'
        if i%2 == 0:
            post_type='stry'
        if i%5 == 0:
            ver=False
        if i%4 == 0:
            post_type='proj'
        p = Post(creator=email, title = str(i) + title, text_content=content, type=post_type, verified = ver)
        p.set_url( tag_maker('_', p) )
        p.save()
    return


