from django.template import Context, loader
from django.shortcuts import render_to_response

def index(request):
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    
    return render_to_response("home/index.html",{'logparams': logparams}                    
        )
    
