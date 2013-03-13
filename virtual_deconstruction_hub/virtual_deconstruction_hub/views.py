from django.template import RequestContext
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
    
    return render_to_response("statistics/statistics_main.html",{'logparams': logparams},
                              context_instance=RequestContext(request)                   
        )
    
