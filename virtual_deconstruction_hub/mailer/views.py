from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext
from django.core.mail import send_mail
	
# Page to Contact a seller
def contact_seller(request):
	if request.POST.get('send_email'):
		fromEmail = request.POST.get('emailTxt')
		subject = request.POST.get('emailSubject')
		message = request.POST.get('emailMsg')
		send_mail(subject, message, fromEmail, ['gharoldson@gmail.com'], fail_silently=False)
		response = HttpResponse("Email Sent Successfully")
		return response
	else:
		return render_to_response("mailer/contact_seller.html",context_instance=RequestContext(request))