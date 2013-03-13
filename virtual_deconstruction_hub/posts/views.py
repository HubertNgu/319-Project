
# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.template.defaulttags import csrf_token
from django.template import RequestContext
from django.contrib.auth.models import User
from posts.models import Post
from django.contrib.auth import authenticate,login,get_user
from django.http import  HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from userprofile.models import UserProfile 
from verificationapp.models import VerificationApp
import string
import random
from postpictures.models import *
from fileupload.views import handle_uploaded_file
from django.forms import ModelForm

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
        post = Post()
        post.type = post_type        
        form = PostForm(instance=post)
        #form = form.as_table()
        return render_to_response("posts/posts_new.html", { 'form': form}, context_instance=RequestContext(request))
    
    
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))
    
def verify_post(request):
        message = "Your post has been verified and will now be visible to others."
        return render_to_response("posts/verification.html",context_instance=RequestContext(request), message=message)
def index(request):
    user = None
    if request.user.is_authenticated():
        if request.user.username == "admin":
            user = "admin"
    return render_to_response("posts/blogs_index.html", {'user':user}, context_instance=RequestContext(request))
            
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

