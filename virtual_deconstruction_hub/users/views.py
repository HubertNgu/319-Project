from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
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
import string
import random

def index(request):
    if request.user.is_authenticated():
       return redirect('virtual_deconstruction_hub.views.index')
    elif request.method == 'POST':
        usernamepost = request.POST.get('username')
        passwordpost = request.POST.get('password')
        user = authenticate(username=usernamepost, password=passwordpost)
        if user is not None:
            if user.is_active:
                 login(request, user)
                 return redirect('virtual_deconstruction_hub.views.index')
            else:
                print "Your account has been disabled!"
        else:
            print "Your username and password were incorrect."
            return render_to_response("users\loginnotsuccessful.html")
    else:
        form = AuthenticationForm()
        return render_to_response("users\login.html", {
        'form': form},context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    response = redirect('virtual_deconstruction_hub.views.index')
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
            #add email to include in querystring username and verification. i.e(www.example.com/users/verifyemail/username/verification code)
            #verification code is under variable verification code
            return   render_to_response("users/verification.html",context_instance=RequestContext(request))
    else:
        
        return render_to_response("users/signup.html",context_instance=RequestContext(request))

def verification(request):
     return render_to_response("users/verification.html",context_instance=RequestContext(request))
 
def verifyemail(request,username, verification):
    verify = VerificationApp(username = username)
    if verify.verificationcode == verification:
        verifyuser = UserProfile(username = username)
        verifyuser.isverified = true
        verifyuser.save()
        return redirect('virtual_deconstruction_hub.views.index')
    else: return redirect('virtual_deconstruction_hub.users.views.verifyfail')

def verifyfail(response):
      return render_to_response("users/verifyfail.html",context_instance=RequestContext(request))
     
    

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def editaccount(request):
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
        return redirect("users.views.myaccount")
    
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
                                                      'description':description,},context_instance=RequestContext(request))

def myaccount(request):
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
    return render_to_response("users\myaccount.html",{'username':username,
                                                      'firstname':firstname,
                                                      'lastname':lastname,
                                                      'email':email,
                                                      'address':address,
                                                      'city':city,
                                                      'phone':phone,
                                                      'province':province,
                                                      'description':description,},context_instance=RequestContext(request))