'''
 Integration tests for the virtual deconstruction hub.

 @author Hubert Ngu
'''

import logging
from django.test import TestCase
from datetime import datetime, timedelta
from util import constants

from survey_system import survey_mailer
from survey_system.models import Survey
from listings.models import Listing
from statistics_generator import statistics
from statistics_generator.models import Statistics, StatisticsCategory

class IntegrationTest(TestCase):

	def setUp(self):
		logger = logging.getLogger()
		logger.setLevel(logging.ERROR)
		# These times are in days
		constants.INITIAL_SEND_DELAY = 0
		constants.REPEAT_SEND_DELAY = 0

	def test_listing_to_statisics_no_survey(self):
		listing = Listing(id=1, for_sale='sell', url='test', 
				creator='test@test.com', created=datetime.now(),
				last_modified=datetime.now(), title='test',
				text_content='test', verified=True,
				category='Bricks', price='test',
				address='test street', city='test city',
				flag_count=1, expires=(datetime.now() + timedelta(days=30)),
				expired=1, survey_time_sent=None, uuid='1')
		listing.save()

		# Expect that 0 surveys were sent because no listing are
		# ready to have a survey sent. i.e. this is 1 expired listing.
		expected = 0
		actual = survey_mailer.expire_and_mail_surveys()
		self.assertEqual(expected, actual)

	def test_listing_to_statistics_survey(self):
		listing = Listing(id=1, for_sale='sell', url='test', 
				creator='test@test.com', created=datetime.now(),
				last_modified=datetime.now(), title='test',
				text_content='test', verified=True,
				category='Bricks', price='test',
				address='test street', city='test city',
				flag_count=1, expires=(datetime.now() + timedelta(days=30)),
				expired=0, survey_time_sent=None, uuid='1')
		listing.save()

		# Expect that 1 survey was sent because one listing is
		# ready to have a survey sent.
		expected = 1
		actual = survey_mailer.expire_and_mail_surveys()
		self.assertEqual(expected, actual)

		# Simulate that a survey was submitted
		survey = Survey(id=1, listing_id=1, item='test item', category='Bricks',
				price=3, address='test street', city='test city',
				comments='test comments', time_submitted=datetime.now())
		survey.save()
		listing.survey_time_sent = datetime.now()
		listing.save()

		statistics.generate_statistics()

		stats = Statistics.objects.get(id=1)
		self.assertEqual(1, stats.number_surveys)
		self.assertEqual(1, stats.number_listings)
		self.assertEqual(0, stats.number_buyer_surveys)
		self.assertEqual(1, stats.number_seller_surveys)
		self.assertEqual(0, stats.number_buyer_listings)
		self.assertEqual(1, stats.number_seller_listings)
		self.assertEqual(3, stats.average_transaction_amount)
		self.assertEqual(0, stats.buyer_transaction_amount)
		self.assertEqual(3, stats.seller_transaction_amount)
		self.assertEqual(3, stats.successful_transaction_amount)
		self.assertEqual(0, stats.average_transaction_time)
		self.assertEqual(100, stats.buyer_transaction_success_rate)
		self.assertEqual(100, stats.seller_transaction_success_rate)
		self.assertEqual(100, stats.total_transaction_success_rate)

		stats_categories = StatisticsCategory.objects.filter(statistics_id=1)
		for cat in stats_categories:
			if cat.category == 'Bricks':
				self.assertEqual(1, cat.survey_count)
				self.assertEqual(0, cat.buyer_count)
				self.assertEqual(1, cat.seller_count)
				self.assertEqual(3, cat.amount)
			else:
				self.assertEqual(0, cat.survey_count)
				self.assertEqual(0, cat.buyer_count)
				self.assertEqual(0, cat.seller_count)
				self.assertEqual(0, cat.amount)

	def test_listing_to_statistics_survey_many(self):
		for i in range(255):
			listing_sell = Listing(id=i, for_sale='sell', url='test', 
				creator='test@test.com', created=datetime.now(),
				last_modified=datetime.now(), title='test',
				text_content='test', verified=True,
				category='Bricks', price='test',
				address='test street', city='test city',
				flag_count=1, expires=(datetime.now() + timedelta(days=30)),
				expired=0, survey_time_sent=None, uuid=str(i))
			listing_buy = Listing(id=i+255, for_sale='want', url='test', 
				creator='test@test.com', created=datetime.now(),
				last_modified=datetime.now(), title='test',
				text_content='test', verified=True,
				category='Bricks', price='test',
				address='test street', city='test city',
				flag_count=1, expires=(datetime.now() + timedelta(days=30)),
				expired=0, survey_time_sent=None, uuid=str(i+255))
			listing_sell.save()
			listing_buy.save()

		expected = 255*2
		actual = survey_mailer.expire_and_mail_surveys()
		self.assertEqual(expected, actual)

		# Simulate that a survey was submitted
		for i in range(255*2):
			survey = Survey(id=i, listing_id=i, item='test item', category='Bricks',
				price=3, address='test street', city='test city',
				comments='test comments', time_submitted=datetime.now())
			survey.save()
			listing = Listing.objects.get(id=i)
			listing.survey_time_sent = datetime.now()
			listing.save()

		statistics.generate_statistics()

		stats = Statistics.objects.get(id=1)
		self.assertEqual(510, stats.number_surveys)
		self.assertEqual(510, stats.number_listings)
		self.assertEqual(255, stats.number_buyer_surveys)
		self.assertEqual(255, stats.number_seller_surveys)
		self.assertEqual(255, stats.number_buyer_listings)
		self.assertEqual(255, stats.number_seller_listings)
		self.assertEqual(3, stats.average_transaction_amount)
		self.assertEqual(255*3, stats.buyer_transaction_amount)
		self.assertEqual(255*3, stats.seller_transaction_amount)
		self.assertEqual(510*3, stats.successful_transaction_amount)
		self.assertEqual(0, stats.average_transaction_time)
		self.assertEqual(100, stats.buyer_transaction_success_rate)
		self.assertEqual(100, stats.seller_transaction_success_rate)
		self.assertEqual(100, stats.total_transaction_success_rate)

		stats_categories = StatisticsCategory.objects.filter(statistics_id=1)
		for cat in stats_categories:
			if cat.category == 'Bricks':
				self.assertEqual(510, cat.survey_count)
				self.assertEqual(255, cat.buyer_count)
				self.assertEqual(255, cat.seller_count)
				self.assertEqual(510*3, cat.amount)
			else:
				self.assertEqual(0, cat.survey_count)
				self.assertEqual(0, cat.buyer_count)
				self.assertEqual(0, cat.seller_count)
				self.assertEqual(0, cat.amount)


				