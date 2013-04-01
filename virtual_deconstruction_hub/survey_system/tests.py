'''
 Unit tests for the survey_system app.

 @author Hubert Ngu
'''
from util import constants
from datetime import datetime, timedelta
from listings.models import Listing
from survey_system import survey_mailer, views

from django.http import Http404, HttpRequest
from django.test import TestCase

class SurveyTest(TestCase):

	def setUp(self):
		# These times are in days
		constants.INITIAL_SEND_DELAY = 1
		constants.REPEAT_SEND_DELAY = 1
    
   	def test_is_survey_ready_false_expired(self):
   		listing = Listing(expired=True, survey_time_sent=datetime.now(),
   					created=datetime.now())
   		actual = vars(survey_mailer)['__is_survey_ready'](listing)
   		self.assertFalse(actual)

   	def test_is_survey_ready_false_not_passed_resend(self):
   		listing = Listing(expired=False, survey_time_sent=datetime.now(),
   					created=datetime.now())
   		actual = vars(survey_mailer)['__is_survey_ready'](listing)
   		self.assertFalse(actual)

   	def test_is_survey_ready_true_never_sent(self):
   		listing = Listing(expired=False, survey_time_sent=None,
   						created=datetime.now() - timedelta(days=1))
   		actual = vars(survey_mailer)['__is_survey_ready'](listing)
   		self.assertTrue(actual)

   	def test_is_survey_ready_true_resend_ready(self):
   		listing = Listing(expired=False, 
   						survey_time_sent=datetime.now() - timedelta(days=1),
   						created=datetime.now() - timedelta(days=7))
   		actual = vars(survey_mailer)['__is_survey_ready'](listing)
   		self.assertTrue(actual)

   	def test_get_valid_listing_raise404(self):
   		self.assertRaises(Http404, vars(views)['__get_valid_listing'], '1')

   	def test_get_valid_listing_found(self):
   		listing = Listing(uuid='123')
   		listing.save()
   		# This should not raise an exception
   		vars(views)['__get_valid_listing']('123')

   	def test_survey_expired(self):
   		listing = Listing(expired=1, uuid='123')
   		listing.save()
   		request = HttpRequest()
   		request.method = 'GET'
   		response = vars(views)['survey'](request, '123')
   		self.assertTrue('Survey for this listing has expired' 
   				in vars(response)['_container'][0])

   	def test_survey_get(self):
   		listing = Listing(expired=0, uuid='123', category='Bricks', 
   					id=1, city='Hope', address='747 Fort Street',
   					title='selling stuff')
   		listing.save()
   		request = HttpRequest()
   		request.method = 'GET'
   		response = vars(views)['survey'](request, '123')
   		html = vars(response)['_container'][0]
   		self.assertTrue('selected="selected">Bricks</option>' in html)
   		self.assertTrue('selected="selected">Hope</option>' in html)
   		self.assertTrue('value="747 Fort Street"' in html)
   		self.assertTrue('value="selling stuff"' in html)

   	def test_survey_post_invalid(self):
   		listing = Listing(expired=0, uuid='123', category='Bricks', 
   					id=1, city='Hope', address='747 Fort Street',
   					title='selling stuff')
   		listing.save()
   		request = HttpRequest()
   		request.method = 'POST'
   		response = vars(views)['survey'](request, '123')
   		html = vars(response)['_container'][0]
   		self.assertTrue('This field is required' in html)