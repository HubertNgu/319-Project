# Create your views here.
from django.http import HttpRequest
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.defaulttags import csrf_token
from django.template import RequestContext
from django.contrib.auth.models import User
from posts.models import Post
from django.contrib.auth import authenticate,login,get_user
from django.shortcuts import redirect
from verificationapp.models import VerificationApp
from postpictures.models import *
from fileupload.views import handle_uploaded_file
from posts.models import PostForm
from django import forms
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
import re
import string
import random

PAGE_SIZE = settings.RESULTS_PAGE_SIZE

def new_post(request, post_type):
    #action for submit button
    submit_action = "/posts/" + post_type + "/new"
    if request.method == 'GET':
        form = PostForm(instance=Post())
        form_args = {'form':form, 'submit_action':submit_action, 'post_type':post_type}
        return render_to_response("posts/posts_new.html", form_args, context_instance=RequestContext(request))
    if request.method == 'POST':
                
        post_form = PostForm(request.POST)
        #if post_form valid, process new post
        if post_form.is_valid():
            # write to db and return post object
            post = post_form.save(commit=False)
            post.type = post_type.lower()
            post.url = tag_maker("_", post.title)
            #check that url is unique in db, if url already exists
            # append a random 10 char string to the end
            if Post.objects.filter(url=post.url).count() > 0:
                post.url = tag_maker("_", post.url + ' ' + random_string_generator(10))

            post_url = post.url
            post_url = HttpRequest.build_absolute_uri(request, post_url)
            
            #===================================================================
            # if request.user.is_authenticated():
            #    post.verified = True  
            #===================================================================
            post.save()
            form_args = {'post':post, 'post_url': post_url}
            
            if request.GET.get('photo_upload') is 1:
            # if phot_upload tag triggered, save the current post as object in db
            # thentake current photo from form, save to child db table for post
            # photo and hold on to form, but render a new photo upload form and 
            # repeat as long as photo_pload tag triggered, once photo_upload no longer
            # trigered, redirect to success page  
                pass
           

            ## fill in test data in db: writes 100 post objects of same type as whatever new form you are entering
            email = 'sean@testing.com'
            title = ' Test Title '
            content = ' - Bah blah blah blahahab labalaba hbaalavhgvsha balobuebfuewbfuebfue jefbuefuewbfuewbfuwefbuwebfuweb fiunbefiuwef uefbuwefbwuefbeufb;efuebf'
            for i in xrange(0,100):
                p = Post(creator=email, title=post_type.upper()+title+str(i),text_content=str(i)+content, type=post_type.lower(), verified=True)
                p.save()

            if post.verified:
                # if post is already verified, redirect user to their newly created post
                return redirect(post.url, context_instance=RequestContext(request))

            # create a verification/edit link and send with mailer then direct to success message page
            #still need ot do the verification link
            return render_to_response("posts/new_post_success.html", form_args, context_instance=RequestContext(request))
        else:
            # if form submission not valid, redirect back to form with error messages
            form_args = {'form':post_form, 'submit_action':submit_action}
            return render_to_response("posts/posts_new.html", form_args, context_instance=RequestContext(request))


def verify_post(request, post_type):        
    #message = "Your post has been verified and will now be visible to others."
    post_id = request.GET.get('post_id')
    uuid = request.GET.get('uuid')
    post = None
    try:
        post = get_object_or_404(Post, id=str(post_id))
    except:
        raise Http404
    
    if post and (post.uuid == str(uuid)):
        post.verified = True
        post.save()
        post_url = HttpRequest.build_absolute_uri(request, post.url)
        return redirect(post_url,context_instance=RequestContext(request))
    else:
        # redirect to a failure page of some kind?
        raise Http404

#===============================================================================
# def index(request):
#    user = None
#    if request.user.is_authenticated():
#        if request.user.username == "admin":
#            user = "admin"
#    return render_to_response("posts/blogs_index.html", {'user':user}, context_instance=RequestContext(request))
#===============================================================================
            
    
def posts_index(request, post_type):
    query = Post.objects.filter(type=post_type).filter(verified=True).order_by('-created')
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
    template_paths = {'proj': 'posts/projects_list.html', 'blog': 'posts/blogs_list.html', 'stry': 'posts/stories_list.html'}
    return render_to_response(template_paths.get(post_type),{'posts': posts}, context_instance=RequestContext(request))
        
def posts_specific(request, post_type, tag):
    tag.lower()
    if request.method == 'GET':
        query = get_object_or_404(Post, url=tag)
        #query = Post.objects.get(url=tag, type=post_type)
        if query.verified:
            form = PostForm(instance=query)
            template_paths = {'proj': 'posts/projects_individual.html', 'blog': 'posts/blogs_individual.html', 'stry': 'posts/stories_individual.html'}
            return render_to_response(template_paths.get(post_type),{'post': form}, context_instance=RequestContext(request))
        else:
            raise Http404()        
                                                                                                        
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = PostPictures(photo = request.FILES['picture'], postid = 1 )
            photo.save()
            return render_to_response('posts/posts_new.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = UploadForm()
        return render_to_response('uploadfile/upload.html', {'form': form}, context_instance=RequestContext(request))
        
#===============================================================================
# Takes in a string and removes any no a-z,A-Z,0-9 characters and replaces all
# spaces with the given Space_replacement_char then returns the string in all
# lowercase.
#===============================================================================
def tag_maker(space_replacement_char, tag_string):
    return re.sub(r'\W+', '', tag_string.lower().replace (" ", space_replacement_char ))

def random_string_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
>>>>>>> Commiting work done by Sean

