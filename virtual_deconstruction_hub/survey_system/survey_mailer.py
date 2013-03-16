from util import constants
from listings.models import Listing
from survey_system.models import Survey
from mailer.views import send_survey_email

from datetime import datetime, timedelta
from django.contrib.sites.models import Site

def get_initial_send_delay():
	return timedelta(days=int(constants.INITIAL_SEND_DELAY))

def get_repeat_send_delay():
	return timedelta(days=int(constants.REPEAT_SEND_DELAY))

def is_survey_ready(listing):
	return (listing.survey_time_sent is None and 
		datetime.utcnow() > listing.created + get_initial_send_delay()) or \
		(datetime.utcnow() > listing.survey_time_sent + get_repeat_send_delay())

def filter_ready_surveys(listings):
	return [listing for listing in listings if is_survey_ready(listing)]

def expire_listings():
	listings = Listing.objects.filter(expired=False)
	for listing in listings:
		listing.expired =  datetime.utcnow() > listing.expires
		listing.save()

def mail_surveys():
	listings = Listing.objects.filter(expired=False)
	ready_surveys = filter_ready_surveys(listings)
	for listing in ready_surveys:
		survey_url = '%s/survey/%s' % (constants.SITE, listing.survey_id)	
		send_survey_email(survey_url, listing.creator)