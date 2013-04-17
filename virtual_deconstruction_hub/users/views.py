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
from users.models import UserProfile 
from verificationapp.models import VerificationApp
from mailer.views import send_signup_verification_email
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from listings.models import Listing
from posts.models import Post
from django.conf import settings
from django.contrib.sites.models import Site
import string
import random
import logging
from django.http import Http404  

logger = logging.getLogger(__name__)

#PAGE_SIZE = int(constants.listings_results_page_size)
PAGE_SIZE = int(settings.LISTINGS_PAGE_SIZE)

def index(request):
    #this view is used to login the user
    #get the previous page for redirect later
    prevPage = request.GET.get('prevPage')
    #if there is no previous page, redirect to home page
    if prevPage is None:
        prevPage = '/'
    #if user is already logged in, redirect to their my account page
    if request.user.is_authenticated():
       return redirect('users.views.myaccount')
    elif request.method == 'POST':
        usernamepost = request.POST.get('username')
        passwordpost = request.POST.get('password')
        #check to see if user is verified, if not, redirect to must verify page. 
        if UserProfile.objects.filter(username = usernamepost).exists():
            checkverified = UserProfile.objects.get(username= usernamepost)
            if checkverified.isverified == False:
                return render_to_response("users/mustverify.html",context_instance=RequestContext(request))
        user = authenticate(username=usernamepost, password=passwordpost)
        #if there is no username and password that is in the system, return an 
        #error message telling them that their password or username is wrong
        if user is None:
            errormessage =  "Your email and/or password were incorrect."
            return render_to_response("users/login.html",{'errormessage':errormessage},context_instance=RequestContext(request))   
        #if user is verified and exists, redirect them to the previous page
        login(request, user)
        return redirect(prevPage) 
    else:
        return render_to_response("users/login.html", {'prevPage':prevPage}, context_instance=RequestContext(request))
    raise Http404
#this view is used to logout a user
def logout_user(request):
    #get the previous page for redirect. If user did not visit a previous page, then redirect 
    #to home page
    #logout the user and redirect to home page.
    logout(request)
    response = redirect('/')
    response.delete_cookie('user_location')
    return response
#this view handles all the signup functionality 
def signup(request):
    errormessage = None
    #if the request type is a post
    if request.method == 'POST':
        #do checks to make sure all required fields are entered
        checkusername = request.POST.get("email")
        if checkusername == None:
             errormessage = "You must select an email"
             return render_to_response("users\signup.html",{'errormessage':errormessage},context_instance=RequestContext(request))
        if request.POST.get('password') == None:
             errormessage = "You must choose a password"
             return render_to_response("users\signup.html",{'errormessage':errormessage},context_instance=RequestContext(request))
        if request.POST.get('password') != request.POST.get('confirmpassword'):
          errormessage = "Your passwords do not match"
          return render_to_response("users\signup.html",{'errormessage':errormessage},context_instance=RequestContext(request))
      #if that username has been taken, return error message
        try: 
             User.objects.get(username = checkusername) 
             errormessage = "That email has been taken"
             return render_to_response("users\signup.html",{'errormessage':errormessage},context_instance=RequestContext(request))
        except: 
            #else get all the required information required for the registration
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            phoneno = request.POST.get('phone')
            address = request.POST.get('address')
            province = request.POST.get('province')
            city = request.POST.get('city')
            user = User.objects.create_user(checkusername,email,password)
            user = authenticate(username=checkusername, password=password)
            #create new user with all the information
            profile = UserProfile( username = checkusername, firstname=firstname, lastname=lastname,  province= province, phoneno = phoneno, city = city, address = address, isverified = 0)
            profile.save()
            #generate a verification code
            verificationcode = id_generator()
            verificationapp = VerificationApp(username = checkusername, verificationcode = verificationcode)
            verificationapp.save()
            # generate verify url that user needs to click to activate account
            verify_url = 'http://%s/myaccount/verifyemail/?username=%s&verificationcode=%s' % (Site.objects.get_current(), checkusername, verificationcode)
            #send verification email
            send_signup_verification_email(verify_url, email, firstname)
            logtext = "Login"
            accounttext = "Sign Up"
            logparams=[logtext,accounttext]
            return render_to_response("users/verification.html", {'logparams' : logparams }, context_instance=RequestContext(request))
    else:
        
        return render_to_response("users/signup.html",context_instance=RequestContext(request))
    raise Http404
def verification(request):
    #if user is already logged in and authenticated, then redirec tthem to their account page
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
        #else send them to the verification page
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
        return render_to_response("users/verification.html", {'logparams' : logparams}, context_instance=RequestContext(request))
    raise Http404
 #this view handles the verification of the user
def verifyemail(request):
    
    username = request.GET.get('username')
    verification = request.GET.get('verificationcode')
    #check to see if verification code is correct
    try:
        verify = VerificationApp.objects.get(username = username, verificationcode = verification)
    except:
        verify = None
        #if verification code exists then activate the user and redirect them to their account page
    if verify != None:
        verifyuser = UserProfile.objects.get(username = username)
        verifyuser.isverified = True
        verifyuser.save()
        verify.delete()
        return redirect("/myaccount/login")
    else: return redirect('users.views.verifyfail')
    raise Http404
    
def verifyfail(request):
      return render_to_response("users/verifyfail.html",context_instance=RequestContext(request))
     #generates a random 10 char string used as a verification code
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
#this view handles the users ability to edit their account
def editaccount(request):
    #if user is logged in, provide options for  going to my account and logging out.
    #if user is not logged in, then provide abilirty to sign up
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
        return render_to_response("users/login.html",{'logparams':logparams},context_instance=RequestContext(request))
        
    user =request.user
    username = request.user.username
    #get information of the user
    profile = UserProfile.objects.get(username = username) 
    if request.method == "POST":
        #get variables from post
        email = username
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
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
        #save profile with all edited items
        profile.save()
        if (password != None and password != ''):
            u = User.objects.get(username__exact=username)
            u.set_password(password)
            u.save()
            
        return redirect('/myaccount/profile')
    
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
        return render_to_response("users/editaccount.html",{'username':username,
                                                      'firstname':firstname,
                                                      'lastname':lastname,
                                                      'email':email,
                                                      'address':address,
                                                      'city':city,
                                                      'phone':phone,
                                                      'province':province,
                                                      'description':description,
                                                      'logparams' : logparams},context_instance=RequestContext(request))

    raise Http404
#this view gets all the infomation for a user
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
        return render_to_response("users/login.html",{'logparams':logparams},context_instance=RequestContext(request))
         
    if request.method == 'POST':
        return redirect("users.views.editaccount")
    #get all the information of the user
    username = request.user.username
    email = request.user.email
    try:
        profile = UserProfile.objects.get(username = username) 
    except: 
        profile = UserProfile( username = username,  province='', phoneno ='', city = '', address ='', isverified = 1)
        profile.save()
    address = profile.address
    city = profile.city
    phone = profile.phoneno
    province = profile.province
    description = profile.description
    firstname = profile.firstname
    lastname = profile.lastname
    return render_to_response("users/profile.html",{'username':username,
                                                      'firstname':firstname,
                                                      'lastname':lastname,
                                                      'email':email,
                                                      'address':address,
                                                      'city':city,
                                                      'phone':phone,
                                                      'province':province,
                                                      'description':description,
                                                      'logparams' : logparams},context_instance=RequestContext(request))
    raise Http404
#this view gets all the listings that the user has  
                                          
def listings(request):
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
        #get all the listings that the user has created
        listings_list = Listing.objects.filter(creator = request.user.email).order_by('-created')
        #return list with 25 per page
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
        return render(request, "users/listings.html", { "listings" : listings, 'logparams' : logparams})
    else:
        return redirect("/myaccount/login")
    raise Http404
def posts(request, post_type):
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
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
        return render(request, "users/posts.html", { "posts" : posts, "post_type" : post_type, 'logparams' : logparams})
    else:
        return redirect("/myaccount/login")
    raise Http404
