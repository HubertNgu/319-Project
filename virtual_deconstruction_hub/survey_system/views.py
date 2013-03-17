'''
views.py class for the survey survey_system

@author Hubert Ngu
'''
import logging
from listings.models import Listing
from survey_system.models import Survey

from django.contrib.sites.models import Site
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.defaulttags import csrf_token
from django.template import RequestContext, loader
from django.shortcuts import redirect

def survey(request, survey_id):
	try:
		listing = Listing.objects.get(survey_id=survey_id)
	except:
		raise Http404

	if request.method == 'GET':
		if listing.expired:
			return render_to_response('survey_system/expired.html',
				context_instance=RequestContext(request))
		else:
			return render_to_response("survey_system/survey.html",
				{ 'survey_id' : survey_id },
				context_instance=RequestContext(request))
	elif request.method == 'POST':
		# Grab data
		item = request.POST.get('item')
		category = request.POST.get('category')
		quantity = request.POST.get('quantity')
		price = request.POST.get('price')
		location = request.POST.get('location')
		comments = request.POST.get('comments')

		error_message = str()

		# If any of the required fields are empty, append onto the error_message
		if item is None:
			error_message += 'Please enter the name of the item\n'
		if category is None:
			error_message += 'Please enter the category of the item\n'
		if quantity is None:
			error_message += 'Please enter the quantity of the item\n'
		if price is None:
			error_message += 'Please enter the price of the item\n'
		if location is None:
			error_message += 'Please enter the location of the transaction\n'

		# If there were any errors then return the error response
		if error_message != str():
			return render_to_response('survey_system\survey.html',
				{ 'error_message' : error_message },
				context_instance=RequestContext(request))

		survey = Survey(item=item, category=category, quantity=quantity, 
			price=price, location=location, comments=comments, listing_id=listing.id)
		survey.save()
		listing.expired = 1
		listing.save()
		return render_to_response('survey_system/successful.html',
			context_instance=RequestContext(request))
	else:
		raise Http404