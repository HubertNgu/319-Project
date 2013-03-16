from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext
from django.core.mail import send_mail
from django.template.loader import render_to_string
from mailer.models import Email

CONTACT_EMAIL = 0
SIGNUP_VERIFY = 1
LISTING_VERIFY = 2
SURVEY_EMAIL = 3
	
SUBJECT_MAPPINGS = {'signup' : 'Virtual Deconstruction Hub - Sign Up Verification',
                    'survey' : 'Virtual Deconstruction Hub - Survey',
                    'proj' : 'Virtual Deconstruction - New Project Idea',
                    'blog' : 'Virtual Deconstruction - New Blog Post',
                    'stry' : 'Virtual Deconstruction - New Success Story',
                    'list' : 'Virtual Deconstruction - New Listing'}
                 
    
POST_MAPPINGS = {'proj': 'Project Idea', 
                 'blog' : 'Blog Post', 
                 'stry' : 'Success Story',
                 'list' : 'Listing'}
    
# Page to Contact a seller
def send_contact_email(fromEmail, subject, message):
    send_mail(sub, msg, fromEmail, ['gharoldson@gmail.com'], fail_silently=False)
			
    email = Email(to_email='gharoldson@gmail.com', from_email=fromEmail,subject=sub,message=msg,email_type=CONTACT_EMAIL)
    email.save()		
    return    
        
def send_survey_email(url, userEmail):
    sub = SUBJECT_MAPPINGS.get('survey')
    context = {"url" : url}
    msg = render_to_string('mailer/surveyTemplate.txt', context)
    fromEmail = "from@email.com"
    send_mail(sub, msg, fromEmail, [userEmail], fail_silently=False)
    
    email = Email(to_email=userEmail, from_email=fromEmail,subject=sub,message=msg,email_type=SIGNUP_VERIFY)
    email.save()
    return
   
def send_signup_verification_email(url, userEmail):
    sub = SUBJECT_MAPPINGS.get('signup')
    context = {"url": url }
    msg = render_to_string('mailer/signupTemplate.txt', context)
    fromEmail = "from@email.com"
    send_mail(sub, msg, fromEmail, [userEmail], fail_silently=False)
			  
    email = Email(to_email=userEmail, from_email=fromEmail,subject=sub,message=msg,email_type=SIGNUP_VERIFY)
    email.save()
    return
	
def send_post_verification_email(url, userEmail, postType):
    sub = SUBJECT_MAPPINGS.get(postType)
    context = {"url" : url, "object" : POST_MAPPINGS.get(postType)}
    msg = render_to_string('mailer/postTemplate.txt', context)
    fromEmail = "from@email.com"
    send_mail(sub, msg, fromEmail, [userEmail], fail_silently=False)
    
    email = Email(to_email=userEmail, from_email=fromEmail,subject=sub,message=msg,email_type=SIGNUP_VERIFY)
    email.save()   
    return