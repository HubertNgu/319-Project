'''
views.py class for the survey survey_system

@author Hubert Ngu
'''
import logging
from listings.models import Listing
from survey_system.models import Survey, SurveyForm
from django.contrib.sites.models import Site
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.defaulttags import csrf_token
from django.template import RequestContext, loader
from django.shortcuts import redirect

def survey(request, survey_id):
	try:
		listing = Listing.objects.get(uuid=survey_id)
	except:
		raise Http404

	if request.method == 'GET':
		if listing.expired:
			return render_to_response('survey_system/expired.html',
				context_instance=RequestContext(request))
		else:
			form = SurveyForm(instance=Survey(), 
				initial={'category' : listing.category, 'listing_id' : listing.id})
			form_args = { 'form' : form, 
							'submit_action' : '/survey/%s' % survey_id}
			return render_to_response('survey_system/survey.html', form_args,
				context_instance=RequestContext(request))
	elif request.method == 'POST':
		form = SurveyForm(request.POST,
			initial={'category' : listing.category, 'listing_id' : listing.id})
		if form.is_valid():
			form.listing_id = listing.id
			form.save()
			listing.expired = 1
			listing.save()
			return render_to_response('survey_system/successful.html',
				context_instance=RequestContext(request))
		else:
			form_args = {'form' : form,
							'submit_action' : '/survey/%s' % survey_id}
			return render_to_response('survey_system/survey.html', form_args,
				context_instance=RequestContext(request))
	else:
		raise Http404
