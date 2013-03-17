# Create your views here.
from django.http import HttpRequest
from django.http import Http404
from django.shortcuts import render_to_response
#from django.template.defaulttags import csrf_token
from django.template import RequestContext
#from django.contrib.auth.models import User
from posts.models import Post
#from django.contrib.auth import authenticate,login,get_user
from django.shortcuts import redirect
#from verificationapp.models import VerificationApp
#from postpictures.models import *
#from fileupload.views import handle_uploaded_file
from posts.models import PostForm, EditPostForm
#from django import forms
from util import constants
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
import re
import string
import random
from postpictures.models import UploadForm, PostPictures
from mailer.views import send_post_verification_email
from django.contrib.sites.models import Site

#PAGE_SIZE = int(constants.RESULTS_PAGE_SIZE)
PAGE_SIZE = settings.RESULTS_PAGE_SIZE

TEMPLATE_PATHS = {'proj_list': 'posts/projects_list.html', 'blog_list': 'posts/blogs_list.html', 'stry_list': 'posts/stories_list.html',
                  'proj_single': 'posts/projects_individual.html', 'blog_single': 'posts/blogs_individual.html', 'stry_single': 'posts/stories_individual.html',
                  'posts_new': 'posts/posts_new.html',
                  'posts_success':'posts/new_post_success.html',
                  'posts_upload': 'uploadfile/upload.html',
                  }
URL_PATHS = {'posts_edit-verify': '/posts/edit-verify',
             'posts_root': '/posts/',
             'blog_new': '/posts/blog/new',
             'proj_new': '/posts/proj/new',
             'stry_new': '/posts/stry/new'}

POST_TYPE_TITLES = {'blog': "Blog", 'proj': "Project Ideas", "stry": "Success Stories", 'upload': "Upload"}

MESSAGES = {'verified_post': "Your post has been verified and will be displayed on the site. You can make changes to your post here if you wish.",
            'edit_success': "Your changes have been saved. You can make further changes to your post if you wish."}

def new_post(request, post_type):
    post_type = str(post_type.lower())
    #action for submit button
    submit_action = URL_PATHS.get(post_type+'_new')
    if request.method == 'GET':
        form = PostForm(instance=Post())
        form_args = {'form':form, 'submit_action':submit_action, 'message':None, 'post_type_title':POST_TYPE_TITLES.get(post_type)}
        return render_to_response(TEMPLATE_PATHS.get("posts_new"), form_args, context_instance=RequestContext(request))
    if request.method == 'POST':
                
        post_form = PostForm(request.POST)
        #if post_form valid, process new post
        if post_form.is_valid():
            # write to db and return post object
            post = post_form.save(commit=False)
            post.set_type(post_type.lower())
            post.set_url( tag_maker("_", post) )
            post_url = post.get_url()
            post_url = HttpRequest.build_absolute_uri(request, post_url)
            
            #===================================================================
            # if request.user.is_authenticated():
            #    post.verified = True  
            #===================================================================
            post.save()
            form_args = {'post':post, 'post_url': post_url, 'message':None, 'post_type_title':POST_TYPE_TITLES.get(post_type)}
            
            if request.GET.get('photo_upload') is 1:
            # if phot_upload tag triggered, save the current post as object in db
            # thentake current photo from form, save to child db table for post
            # photo and hold on to form, but render a new photo upload form and 
            # repeat as long as photo_pload tag triggered, once photo_upload no longer
            # trigered, redirect to success page  
                pass
           
           #====================================================================
           # Testing - REMOVE LATER - this just creates x # of posts of a given
           # type whenever a single one is created from the web, just used to 
           # populate db for testing purposes
           #====================================================================
            multiple_entries_for_testing(100, post_type)

            if post.is_verified():
                # if post is already verified, redirect user to their newly created post
                return redirect(post.get_url(), context_instance=RequestContext(request))

            # create a verification/edit link and send with mailer then direct to success message page
            user_email = post.get_creator()
            verify_url = '%s/edit-verify?post_id=%s&uuid=%s' % (Site.objects.get_current(), post.id, post.get_uuid())
            send_post_verification_email(verify_url, user_email, post_type)
            return render_to_response(TEMPLATE_PATHS.get("posts_success"), form_args, context_instance=RequestContext(request))
        else:
            # if form submission not valid, redirect back to form with error messages
            form_args = {'form':post_form, 'submit_action':submit_action, 'message':None, 'post_type_title':POST_TYPE_TITLES.get(post_type)}
            return render_to_response(TEMPLATE_PATHS.get("posts_new"), form_args, context_instance=RequestContext(request))


def edit_verify_post(request):  
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
        form_args = {'form':edit_form, 'message': message, 'submit_action': submit_action, 'post_type_title':POST_TYPE_TITLES.get(post.get_type())}
        return render_to_response(TEMPLATE_PATHS.get("posts_new"), form_args, context_instance=RequestContext(request))
        
    if request.method == 'POST':
        edit_form = EditPostForm(request.POST, instance=post)
        #if post_form valid, process new post
        if edit_form.is_valid():
            post_url = HttpRequest.build_absolute_uri(request, edit_form.cleaned_data.get('url'))
            edit_form.save()
            # This redirects back to edit form, should change to a render_to_response with a message that edit successful
            #return redirect(post_url,context_instance=RequestContext(request))
            #return render_to_response(post_url,context_instance=RequestContext(request))
            form_args = {'form':edit_form, 'submit_action':submit_action, 'message':MESSAGES.get('edit_success'), 'post_type_title':POST_TYPE_TITLES.get(post.get_type()), 'post_url': post_url}
            return render_to_response(TEMPLATE_PATHS.get("posts_new"), form_args, context_instance=RequestContext(request))
        else:
            # if form submission not valid, redirect back to form with error messages
            form_args = {'form':edit_form, 'submit_action':submit_action, 'message':None, 'post_type_title':POST_TYPE_TITLES.get(post.get_type())}
            return render_to_response(TEMPLATE_PATHS.get("posts_new"), form_args, context_instance=RequestContext(request))   
    
def posts_index(request, post_type):
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
    form_args = {'posts':posts, 'message': None, 'post_type_title':POST_TYPE_TITLES.get(post_type)}
    return render_to_response(TEMPLATE_PATHS.get(post_type+'_list'),form_args, context_instance=RequestContext(request))
        
def posts_specific(request, post_type, tag):
    post_type = str(post_type.lower())
    tag.lower()
    if request.method == 'GET':
        query = get_object_or_404(Post, url=tag)
        #query = Post.objects.get(url=tag, type=post_type)
        if query.is_verified():
            form = PostForm(instance=query)
            form_args = {'post':form, 'message':None, 'post_type_title':POST_TYPE_TITLES.get(post_type)}
            return render_to_response( TEMPLATE_PATHS.get(post_type+"_single"),form_args, context_instance=RequestContext(request))
        else:
            raise Http404()        
                                                                                                        
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = PostPictures(photo = request.FILES['picture'], postid = 1 )
            photo.save()
            form_args = {'form':form, 'message': None, 'post_type_title':POST_TYPE_TITLES.get('upload') }
            return render_to_response(TEMPLATE_PATHS.get('posts_new'), form_args, context_instance=RequestContext(request))
    else:
        form = UploadForm()
        form_args = {'form':form, 'message': None, 'post_type_title':POST_TYPE_TITLES.get('upload') }
        return render_to_response(TEMPLATE_PATHS.get('posts_upload'), form_args, context_instance=RequestContext(request))
    
def search_posts(request, post_type):
    post_type = str(post_type.lower())
    pass
        
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

def multiple_entries_for_testing(number, type):
    ## fill in test data in db: writes 100 post objects of same type as whatever new form you are entering
    email = 'sean@testing.com'
    title = ' Test Title '

    for i in xrange(0,number):
        content = str(number) + ' - Bah blah blah blahahab labalaba hbaalavhgvsha balobuebfuewbfuebfue jefbuefuewbfuewbfuwefbuwebfuweb fiunbefiuwef uefbuwefbwuefbeufb;efuebf'
        p = Post(creator=email, title=type.upper()+title,text_content=str(i)+content, type=type.lower(), verified=True)
        p.set_url( tag_maker('_', p) )
        p.save()
    return
