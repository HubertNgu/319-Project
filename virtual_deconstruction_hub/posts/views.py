# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
#from django.template.defaulttags import csrf_token
from django.template import RequestContext
#from django.contrib.auth.models import User
from posts.models import *
from listings.models import Listing
#from django.contrib.auth import authenticate,login,get_user
from django.shortcuts import redirect
from django import forms
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
import re
import string
import random
from posts.models import UploadForm, Photo
from mailer.views import send_post_verification_email
from django.contrib.sites.models import Site
from haystack.query import SearchQuerySet
import logging
from util import constants

logger = logging.getLogger(__name__)

#PAGE_SIZE = int(constants.posts_results_page_size)
PAGE_SIZE = 10

TEMPLATE_PATHS = {'proj_list': 'posts/posts_list.html', 'blog_list': 'posts/posts_list.html', 'stry_list': 'posts/posts_list.html',
                  'proj_single': 'posts/posts_single.html', 'blog_single': 'posts/posts_single.html', 'stry_single': 'posts/posts_single.html',
                  'posts_new': 'posts/posts_new.html',
                  'posts_delete': 'posts/posts_delete.html',
                  'posts_edit': 'posts/posts_edit.html',
                  'posts_success':'posts/new_post_success.html',
                  'posts_upload': 'uploadfile/upload.html',
                  }
URL_PATHS = {'posts_edit-verify': '/posts/edit-verify',
             'posts_delete-verify': '/posts/delete-verify/',
             'posts_root': '/posts/',
             'blog_new': '/posts/blog/new',
             'proj_new': '/posts/proj/new',
             'stry_new': '/posts/stry/new'}

POST_TYPE_TITLES = {'blog': "Blog", 'proj': "Project Ideas", "stry": "Success Stories", 'upload': "Upload"}

MESSAGES = {'verified_post': "Your post has been verified and will be displayed on the site. You can make changes to your post here if you wish.",
            'edit_success': "Your changes have been saved. You can make further changes to your post if you wish."}

def new_post(request, post_type):
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    post_type = str(post_type.lower())
    if request.user.is_authenticated() == False:
         return render_to_response("users/not_user.html", {'logparams': logparams}, context_instance=RequestContext(request))
    if post_type == "blog" and request.user.is_superuser == False:
        return render_to_response("users/not_admin.html", {'logparams': logparams}, context_instance=RequestContext(request))
    #action for submit button
    pictureform = UploadForm()
    submit_action = URL_PATHS.get(post_type+'_new')
    if request.method == 'GET':
        form = PostForm(instance=Post(), initial={'creator':request.user.email, 'email_verification':request.user.email})
        if request.user.is_authenticated():
            form.fields['creator'].widget = forms.HiddenInput()
            form.fields['email_verification'].widget = forms.HiddenInput()
           
        
        form_args = {'form':form, 'submit_action':submit_action, 'message':None, 
                     'post_type_title':POST_TYPE_TITLES.get(post_type), 
                     'pictureform':pictureform, 'logparams': logparams}
        return render_to_response(TEMPLATE_PATHS.get("posts_new"), form_args, context_instance=RequestContext(request))
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if request.user.is_authenticated():
            post_form.fields['creator'].widget = forms.HiddenInput()
            post_form.fields['email_verification'].widget = forms.HiddenInput()
        #if post_form valid, process new post
        
        if post_form.is_valid() and request.POST.get("notnewpost") == None:
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
                photolist = Photo.objects.filter(post_id = post.id)
                addanotherprevious = list()
                for o in Photo.objects.filter(post_id = post.id): 
                    addanotherprevious.append(o.photo.name)
            
                form_args = {'form':post_form, 'submit_action':submit_action, 
                              'pictureform': pictureform,
                             'postid' :postid, 'addanotherprevious' : addanotherprevious, 'logparams':logparams}
                return render_to_response("posts/posts_new.html", form_args, context_instance=RequestContext(request))
            
        #====================================================================
        # Testing - REMOVE LATER - this just creates x # of posts of a given
        # type whenever a single one is created from the web, just used to 
        # populate db for testing purposes
        #====================================================================
        #multiple_entries_for_testing(100, post_type)

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


def edit_verify_post(request): 
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
    post = None
    message = None
    try:
        post = get_object_or_404(Post, id=str(post_id))
    except:
        raise Http404
        
    if request.method == 'GET':      
        if not post.is_verified():   
            if post and (post.get_uuid() == str(uuid)):
                post.mark_verified()
                post.save()
                message = MESSAGES.get('verified_post')
#                post_url = HttpRequest.build_absolute_uri(request, post.get_url())
#                return redirect(post_url,context_instance=RequestContext(request))
            else:
                # the post_id and uuid provided do not match anything in db correctly
                # so redirect to 404 as this page doesn't exist for this combination
                raise Http404
        #post verified by this point, render edit page with message
        edit_form = EditPostForm(instance=post)
        delete_button = URL_PATHS.get('posts_delete-verify') + '?post_id=' + str(post.id) + '&uuid=' + uuid
        form_args = {'form':edit_form, 'message': message, 'submit_action': submit_action, 'post_type_title':POST_TYPE_TITLES.get(post.get_type()), 'logparams': logparams, 'post_type': post.get_type(), 'delete_button': delete_button}
        return render_to_response(TEMPLATE_PATHS.get("posts_edit"), form_args, context_instance=RequestContext(request))
        
    if request.method == 'POST':
        edit_form = EditPostForm(request.POST, instance=post)
        #if post_form valid, process new post
        delete_button = URL_PATHS.get('posts_delete-verify') + '?post_id=' + + str(post.id) + '&uuid=' + uuid
        if edit_form.is_valid():
            post_url = HttpRequest.build_absolute_uri(request, edit_form.cleaned_data.get('url'))
            edit_form.save()
            # This redirects back to edit form, should change to a render_to_response with a message that edit successful
            form_args = {'form':edit_form, 'submit_action':submit_action, 'message':MESSAGES.get('edit_success'), 'post_type_title':POST_TYPE_TITLES.get(post.get_type()), 'post_url': post_url, 'post_type': post.get_type(), 'logparams' : logparams, 'delete_button': delete_button}
            return render_to_response(TEMPLATE_PATHS.get("posts_edit"), form_args, context_instance=RequestContext(request))
        else:
            # if form submission not valid, redirect back to form with error messages
            form_args = {'form':edit_form, 'submit_action':submit_action, 'message':None, 'post_type_title':POST_TYPE_TITLES.get(post.get_type()), 'post_type': post.get_type(),  'logparams':logparams, 'delete_button': delete_button}
            return render_to_response(TEMPLATE_PATHS.get("posts_edit"), form_args, context_instance=RequestContext(request))   
    
def posts_index(request, post_type):
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
    
    post_type = str(post_type.lower())
    query = Post.objects.filter(type=post_type).filter(verified=True).order_by('-last_modified')
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
        
def posts_specific(request, post_type, tag):
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    post_type = str(post_type.lower())
    tag.lower()
    if request.method == 'GET':
        query = get_object_or_404(Post, url=tag)
        #query = Post.objects.get(url=tag, type=post_type)
        if query.is_verified():
            form = PostForm(instance=query)
            photos = query.photo_set.all()
            form_args = {'post':form, 'message':None, 'post_type_title':POST_TYPE_TITLES.get(post_type), 'post_type': post_type, 'photos': photos, 'logparams' : logparams}
            return render_to_response( TEMPLATE_PATHS.get(post_type+"_single"),form_args, context_instance=RequestContext(request))
        else:
            raise Http404()   
        
def delete_verify_post(request): 
    if request.method == 'POST':  
        post_id = request.GET.get('post_id')
        uuid = request.GET.get('uuid')
        #action for submit button
        post = get_object_or_404(Post, id=str(post_id))
        post.verified = False
        post.save()
        message = "Your post will no longer be displayed."
        form_args = { "message" : message, }
        return render_to_response(TEMPLATE_PATHS.get("posts_delete"), form_args, context_instance=RequestContext(request))
    else:
        raise Http404
    
def home(request):
    # Checking for logged in user
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    
    #Try to fetch objects from database, if there aren't any, set to none
    try:
        latest_blog = Post.objects.filter(type='blog').latest('created')
    except:
        latest_blog = None
    try:
        blog_photo = latest_blog.photo_set.all()
        blog_photo = blog_photo[0]
    except:
        blog_photo = None
    try:
        listings = Listing.objects.filter(verified=True, expired=False).order_by('-last_modified')[:5]
    except:
        listings = None
    
    # render response form with form_args list of parameters  
    form_args = {'post': latest_blog, 'listings': listings, 'logparams': logparams, 'blog_photo': blog_photo}
    return render_to_response('statistics_generator/home_page.html', form_args, context_instance=RequestContext(request))

                                                                                                        
    
        
#===============================================================================
# Takes in a post and removes any no a-z,A-Z,0-9 characters in the title,
# replaces all spaces with the given Space_replacement_char then returns a
# unique string in all lowercase to use as the relative url
#===============================================================================
def tag_maker(space_replacement_char, post):
    tag = re.sub(r'\W+', '', post.get_title().lower().replace (" ", space_replacement_char ))
    #check that url is unique in db, if url already exists
    # append a random 10 char string to the end
    if Post.objects.filter(url=tag).count() > 0:
        tag = tag + space_replacement_char + random_string_generator(10)
    return tag

def random_string_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))



