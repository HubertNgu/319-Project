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
import re

PAGE_SIZE = settings.RESULTS_PAGE_SIZE

#===============================================================================
# def create_post(request, post_type):
#    errormessage = None
#    if request.method == 'POST':
#        # do something with it? might not need
#        check_email = request.POST.get("email")
#        if check_email == None:
#            errormessage = "You must enter your email"
#            return render_to_response("posts\posts_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
#        #=======================================================================
#        # if request.POST.get('email') != request.POST.get('confirmemail'):
#        #    errormessage = "Your email does not match the email confirmation you entered"
#        #    return render_to_response("posts\posts_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
#        #=======================================================================
#        if request.POST.get('title') == None:
#            errormessage = "You must enter a title"
#            return render_to_response("posts\posts_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
#        if request.POST.get('content') == None:
#            errormessage = "You must enter some content for your post"
#            return render_to_response("posts\posts_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
#        #=======================================================================
#        # if post_type == None:
#        #    errormessage = "You must choose"
#        #    return render_to_response("posts\posts_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
#        #=======================================================================
# 
#       
#        #------------------------------------------------------------------ try:
#            #---------------------- user = User.objects.get(email = check_email)
#            # # Then user already has a verified account and can post without further checks?
#            # # return render_to_response("users\signup.html",{'errormessage':errormessage},context_instance=RequestContext(request))
#        #--------------------------------------------------------------- except:
#            email = request.POST.get('email')
#            title = request.POST.get('title')
#            content = request.POST.get('content')
#            photo1 = request.POST.get('photo1')
#            photo2 = request.POST.get('photo2')
#            photo3 = request.POST.get('photo3')
#            photo4 = request.POST.get('photo4')
#            
#            #===================================================================
#            # user = User.objects.create_user(checkusername,email,password)
#            # user = authenticate(username=checkusername, password=password)
#            # profile = UserProfile( username = checkusername,  province= province, phoneno = phoneno, city = city, address = address, isverified = 0)
#            # profile.save()
#            #===================================================================
#            post = Post(creator=email, title=title, text_content=content, type=post_type)
#            
#            if request.user.is_authenticated():
#                #mark post verified
#                post.mark_verified()
#            else:
#                #need to verify users email before marking post as verified
#                ## NEED TO EXTEND THIS VERIFICATION APP TO WORK FOR USERS,POSTS AND LISTINGS
#                verificationcode = id_generator()
#                verificationapp = VerificationApp(username = email, verificationcode = verificationcode)
#                verificationapp.save()
#                #add email to include in querystring username and verification. i.e(www.example.com/users/verifyemail/username/verification code)
#                #verification code is under variable verification code
#                message = "A verification email has been sent to your email address! Please open up your email and click on the link provided to activate your post."
#                return   render_to_response("posts/verification.html",context_instance=RequestContext(request), message = message)
#    else:
#        
#        return render_to_response("posts/posts_new.html",context_instance=RequestContext(request))
#===============================================================================

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
            post.url = re.sub(r'\W+', '', post.title.lower().replace (" ", "_"))
            #===================================================================
            # need to put a check here that url is unique in db, if url already exists
            # append a random hash of some kind?
            # title has max char of 100, url max of 110 so have 10 extra char for this
            # purpose
            #===================================================================
            post_url = post.url
            post_url = HttpRequest.build_absolute_uri(request, post_url)
            if request.user.is_authenticated():
                post.verified = True  
            post.save()
            form_args = {'post':post, 'post_url': post_url}
           
            #===================================================================
            # ## fill in test data in db: writes 100 post objects of same type as whatever new form you are entering
            # email = 'sean@testing.com'
            # title = ' Test Title '
            # content = ' - Bah blah blah blahahab labalaba hbaalavhgvsha balobuebfuewbfuebfue jefbuefuewbfuewbfuwefbuwebfuweb fiunbefiuwef uefbuwefbwuefbeufb;efuebf'
            # for i in xrange(0,100):
            #    p = Post(creator=email, title=post_type.upper()+title+str(i),text_content=str(i)+content, type=post_type.lower())
            #    p.save()
            #===================================================================
               
            #===================================================================
            # if post.verified:
            #    # if post is already verified, redirect user to their newly created post
            #    return render_to_response(post.url, form_args, context_instance=RequestContext(request))
            # else:
            #    #otherwise direct to success message page
            #===================================================================
            return render_to_response("posts/new_post_success.html", form_args, context_instance=RequestContext(request))
        else:
            # if form submission not valid, redirect back to form with error messages
            form_args = {'form':post_form, 'submit_action':submit_action}
            return render_to_response("posts/posts_new.html", form_args, context_instance=RequestContext(request))
        
#===============================================================================
# def id_generator(size=10, chars=string.ascii_uppercase + string.digits): 
#    return ''.join(random.choice(chars) for x in range(size))
#===============================================================================

#===============================================================================
# def verify_post(request):        
#    message = "Your post has been verified and will now be visible to others."
#    return render_to_response("posts/verification.html",context_instance=RequestContext(request), message=message)
#===============================================================================
#===============================================================================
# def index(request):
#    user = None
#    if request.user.is_authenticated():
#        if request.user.username == "admin":
#            user = "admin"
#    return render_to_response("posts/blogs_index.html", {'user':user}, context_instance=RequestContext(request))
#===============================================================================
            
    
def posts_index(request, post_type):
    query = Post.objects.filter(type=post_type).order_by('-created')
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
        query = Post.objects.get(url=tag, type=post_type)
        if query:
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
        return render_to_response('uploadfile/upload.html', {'form': form}, context_instance=RequestContext(request))# Create your views here.

