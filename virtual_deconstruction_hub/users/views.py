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
    
    if request.method == 'POST':
        form =  UserCreationForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        user = User.objects.create_user(username,email,password)
        usernamepost = request.POST.get('username')
        passwordpost = request.POST.get('password')
        user = authenticate(username=usernamepost, password=passwordpost)
        login(request,user)
            

        return redirect('virtual_deconstruction_hub.views.index')
    else:
        form = UserCreationForm()
        return render_to_response("users\signup.html", {
        'form': form},context_instance=RequestContext(request))