from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response, render
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.template.defaulttags import csrf_token
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,get_user
from django.http import  HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from userprofile.models import UserProfile 
from verificationapp.models import VerificationApp
from mailer.views import send_signup_verification_email
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from listings.models import Listing
from posts.models import Post
from django.conf import settings
import string
import random

#PAGE_SIZE = int(constants.RESULTS_PAGE_SIZE)
PAGE_SIZE = settings.RESULTS_PAGE_SIZE

def index(request):
    if request.user.is_authenticated():
       return redirect('/')
    elif request.method == 'POST':
        usernamepost = request.POST.get('username')
        passwordpost = request.POST.get('password')
        if UserProfile.objects.filter(username = usernamepost).exists():
            checkverified = UserProfile.objects.get(username= usernamepost)
            if checkverified.isverified == False:
                return render_to_response("users\mustverify.html",context_instance=RequestContext(request))
        user = authenticate(username=usernamepost, password=passwordpost)
        if user is None:
            errormessage =  "Your username and/or password were incorrect."
            return render_to_response("users\login.html",{'errormessage':errormessage},context_instance=RequestContext(request))   
        login(request, user)
        return redirect('/')
   
    else:
        return render_to_response("users\login.html",context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    response = redirect('/')
    response.delete_cookie('user_location')
    return response

def signup(request):
    errormessage = None
    if request.method == 'POST':
        checkusername = request.POST.get("username")
        if checkusername == None:
             errormessage = "You must select a username"
             return render_to_response("users\signup.html",{'errormessage':errormessage},context_instance=RequestContext(request))
        if request.POST.get('password') == None:
             errormessage = "You must choose a password"
             return render_to_response("users\signup.html",{'errormessage':errormessage},context_instance=RequestContext(request))
        if request.POST.get('password') != request.POST.get('confirmpassword'):
          errormessage = "Your passwords do not match"
          return render_to_response("users\signup.html",{'errormessage':errormessage},context_instance=RequestContext(request))
        if request.POST.get('email') == None:
             errormessage = "You must enter an email address"
             return render_to_response("users\signup.html",{'errormessage':errormessage},context_instance=RequestContext(request))
       
        try: 
             User.objects.get(username = checkusername) 
             errormessage = "That account name has been taken"
             return render_to_response("users\signup.html",{'errormessage':errormessage},context_instance=RequestContext(request))
        except: 
            email = request.POST.get('email')
            password = request.POST.get('password')
            phoneno = request.POST.get('phone')
            address = request.POST.get('address')
            province = request.POST.get('province')
            city = request.POST.get('city')
            user = User.objects.create_user(checkusername,email,password)
            user = authenticate(username=checkusername, password=password)
            profile = UserProfile( username = checkusername,  province= province, phoneno = phoneno, city = city, address = address, isverified = 0)
            profile.save()
            verificationcode = id_generator()
            verificationapp = VerificationApp(username = checkusername, verificationcode = verificationcode)
            verificationapp.save()
            send_signup_verification_email("http://localhost:8080/users/verifyemail/?username="+ checkusername + "&verificationcode="+ verificationcode, email)
            return render_to_response("users/verification.html",context_instance=RequestContext(request))
    else:
        
        return render_to_response("users/signup.html",context_instance=RequestContext(request))

def verification(request):
     return render_to_response("users/verification.html",context_instance=RequestContext(request))
 
def verifyemail(request):
    username = request.GET.get('username')
    verification = request.GET.get('verificationcode')
    verify = VerificationApp.objects.get(username = username)
    if verify.verificationcode == verification:
        verifyuser = UserProfile.objects.get(username = username)
        verifyuser.isverified = True
        verifyuser.save()
        verify.delete()
        return redirect('virtual_deconstruction_hub.views.index')
    else: return redirect('users.views.verifyfail')

def verifyfail(request):
      return render_to_response("users/verifyfail.html",context_instance=RequestContext(request))
     
    

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def editaccount(request):
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    user =request.user
    username = request.user.username
    profile = UserProfile.objects.get(username = username) 
    if request.method == "POST":
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phoneno = request.POST.get('phone')
        address = request.POST.get('address')
        province = request.POST.get('province')
        city = request.POST.get('city')
        profile.firstname = firstname
        profile.lastname = lastname
        profile.phoneno = phoneno
        profile.address = address
        profile.city = city
        profile.province = province
        profile.save()
        return render_to_response("users\myaccount", {'logparams': logparams})
    
    else:
        username = request.user.username
        email = request.user.email
        address = profile.address
        city = profile.city
        phone = profile.phoneno
        province = profile.province
        description = profile.description
        firstname = profile.firstname
        lastname = profile.lastname
        return render_to_response("users\editaccount.html",{'username':username,
                                                      'firstname':firstname,
                                                      'lastname':lastname,
                                                      'email':email,
                                                      'address':address,
                                                      'city':city,
                                                      'phone':phone,
                                                      'province':province,
                                                      'description':description,
                                                      'logparams' : logparams},context_instance=RequestContext(request))

def myaccount(request):
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    if request.method == 'POST':
        return redirect("users.views.editaccount")
    username = request.user.username
    email = request.user.email
    profile = UserProfile.objects.get(username = username) 
    address = profile.address
    city = profile.city
    phone = profile.phoneno
    province = profile.province
    description = profile.description
    firstname = profile.firstname
    lastname = profile.lastname
    return render_to_response("users\profile.html",{'username':username,
                                                      'firstname':firstname,
                                                      'lastname':lastname,
                                                      'email':email,
                                                      'address':address,
                                                      'city':city,
                                                      'phone':phone,
                                                      'province':province,
                                                      'description':description,
                                                      'logparams': logparams},context_instance=RequestContext(request))

                                                      
def listings(request):
    #    if request.
    listings_list = Listing.objects.filter(creator = request.user.email).order_by('-created')
    paginator = Paginator(listings_list, 25)
    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        listings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        listings = paginator.page(paginator.num_pages)
#    return render_to_response('listings/listings_list.html', {"listings": listings})
    return render(request, "users/listings.html", { "listings" : listings, "username" : request.user.username })
def posts(request, post_type):
    post_type = str(post_type.lower())
    query = Post.objects.filter(type=post_type, creator=request.user.email).order_by('-last_modified')
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
    return render(request, "users/" + post_type + ".html", { "posts" : posts, "username" : request.user.username })

