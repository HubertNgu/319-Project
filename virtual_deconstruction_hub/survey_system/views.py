'''
views.py class for the survey survey_system

@author Hubert Ngu
'''
import logging
from survey_system.models import Survey

from django.shortcuts import render_to_response
from django.template.defaulttags import csrf_token
from django.template import RequestContext, loader
from django.shortcuts import redirect

def submit_survey(request):
	'''
	Submit a survey and store the results into the database

	@param request The HTTP request
	'''
	error_message = str()

	if request.method == 'POST':
		# Grab data
		item = request.POST.get('item')
		quantity = request.POST.get('quantity')
		price = request.POST.get('price')
		comments = request.POST.get('comments')

		# If any of the required fields are empty, append onto the error_message
		if item is None:
			error_message += 'Please enter the name of the item you sold\n'
		if quantity is None:
			error_message += 'Please enter the quantity of the item you sold\n'
		if price is None:
			error_message += 'Please enter the price of the item you sold\n'

		# If there were any errors then return the error response
		if error_message != str():
			return render_to_response('survey_system\survey_system_index.html',
				{ 'error_message' : error_message },
				context_instance=RequestContext(request))

		survey = Survey(item=item, quantity=quantity, price=price, comments=comments)
		survey.save()
		return render_to_response('survey_system/survey_system_successful.html',
			context_instance=RequestContext(request))
	return render_to_response("survey_system/survey_system_index.html",
		context_instance=RequestContext(request))

def successful(request):
	return render_to_response('survey_system/survey_system_successful.html',
		context_instance=RequestContext(request))
