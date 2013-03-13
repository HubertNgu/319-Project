from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext
from django.core.mail import send_mail
from mailer.models import Email
	
# Page to Contact a seller
def contact_seller(request):
	if request.POST.get('send_email'):
		fromEmail = request.POST.get('emailTxt')
		sub = request.POST.get('emailSubject')
		msg = request.POST.get('emailMsg')
		
		send_mail(sub, msg, fromEmail, ['gharoldson@gmail.com'], fail_silently=False)
		
		
		email = Email(to_email='gharoldson@gmail.com', from_email=fromEmail,subject=sub,message=msg,email_type=0)
		email.save()
		
		response = HttpResponse("Email Sent Successfully")
		return response
	else:
		return render_to_response("mailer/contact_seller.html",context_instance=RequestContext(request))