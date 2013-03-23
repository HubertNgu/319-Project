'''
 Views module for the survey system.

 @author Hubert Ngu 
'''

import logging
from listings.models import Listing
from survey_system.models import Survey, SurveyForm

from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

logger = logging.getLogger(__name__)

def __get_valid_listing(uuid):
    '''
    Validates the given uuid for a survey. If we cannot find
    the listing assoicated with the uuid then raise a Http404
    exception. 
    '''
    try:
        listing = Listing.objects.get(uuid=uuid)
    except:
        raise Http404
    return listing

def survey(request, survey_id):
    '''
    Loads the survey view. This function is dynamic as it handles
    loading different html pages based on a GET or POST request
    and the results of the request.

    @param request
                The GET or POST request
    @param survey_id
                The uuid associated with the survey/listing
    '''
    # Validate the listing, if failure then raise Http404
    listing = __get_valid_listing(survey_id)

    # Check if the listing has already been expired.
    # We don't want to allow clients to submit multiple surveys
    # so if it's expired then send them to the expired.html page.
    if listing.expired:
        logger.debug('User attempted to access survey for ' \
            'listing %s but it was already expired', survey_id)
        return render_to_response('survey_system/expired.html',
            context_instance=RequestContext(request))

    # Handle the GET request
    if request.method == 'GET':
        # Generate the SurveyForm for the user to fill out.
        form = SurveyForm(instance=Survey(), 
                initial={ 'category' : listing.category, 'listing_id' : listing.id, 
                          'city' : listing.city, 'address' : listing.address, 
                          'item' : listing.title})
        form_args = { 'form' : form, 'submit_action' : '/survey/%s' % survey_id}
        logger.debug('Generated a SurveyForm for the listing %s', survey_id)
        return render_to_response('survey_system/survey.html', form_args,
                    context_instance=RequestContext(request))

    # Handle the POST request
    elif request.method == 'POST':
        form = SurveyForm(request.POST,
            initial={'category' : listing.category, 'listing_id' : listing.id})
        if form.is_valid():
            form.listing_id = listing.id
            form.save()
            listing.expired = 1
            listing.save()
            logger.debug('Successfully submitted survey for the listing %s', survey_id)
            return render_to_response('survey_system/successful.html',
                context_instance=RequestContext(request))
        else:
            form_args = {'form' : form, 'submit_action' : '/survey/%s' % survey_id}
            return render_to_response('survey_system/survey.html', form_args,
                context_instance=RequestContext(request))

    # Otherwise, something strange has happened so raise Http404
    else:
        raise Http404
