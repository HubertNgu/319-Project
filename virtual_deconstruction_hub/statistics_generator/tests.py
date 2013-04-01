'''
 Unit tests for the statistics_generator app.

 @author Hubert Ngu
'''

from django.test import TestCase
from datetime import timedelta

from survey_system.models import Survey
from listings.models import Listing
from statistics_generator import statistics

class StatisticsTest(TestCase):

    def test_category_rank_empty(self):
        surveys = []
        expected = {}
        actual = vars(statistics)['__category_rank'](surveys)
        self.assertEqual(expected, actual)

    def test_category_rank(self):
        surveys = [ Survey(category='a'), Survey(category='b'),
                    Survey(category='c'), Survey(category='a') ]
        expected = { 'a' : 2, 'b' : 1, 'c' : 1 }
        actual = vars(statistics)['__category_rank'](surveys)
        self.assertEqual(expected, actual)
 
    def test_survey_category_transaction_amount_empty(self):
        surveys = []
        expected = {}
        actual = vars(statistics)['__survey_category_transaction_amount'](surveys)
        self.assertEqual(expected, actual.count)

    def test_survey_category_transaction_amount_diff(self):
        surveys = [Survey(category='a', price=10),
                    Survey(category='b', price=10),
                    Survey(category='c', price=100)]
        expected = { 'a' : 10, 'b' : 10, 'c' : 100 }
        actual = vars(statistics)['__survey_category_transaction_amount'](surveys)
        self.assertEqual(expected, actual.count)

    def test_survey_category_transaction_amount_same(self):
        surveys = [Survey(category='a', price=10),
                    Survey(category='a', price=10),
                    Survey(category='a', price=100)]
        expected = { 'a' : 120 }
        actual = vars(statistics)['__survey_category_transaction_amount'](surveys)
        self.assertEqual(expected, actual.count)

    def test_survey_average_transaction_amount_empty(self):
        surveys = []
        expected = 0
        actual = vars(statistics)['__survey_average_transaction_amount'](surveys)
        self.assertEqual(expected, actual)

    def test_survey_average_transaction_amount_many(self):
        surveys = [Survey(price=100) for _ in range(100)]
        expected = 100
        actual = vars(statistics)['__survey_average_transaction_amount'](surveys)
        self.assertEqual(expected, actual)

    def test_survey_average_transaction_amount(self):
        surveys = [Survey(price=100), Survey(price=50), Survey(price=30)]
        expected = sum([100, 50, 30])/3
        actual = vars(statistics)['__survey_average_transaction_amount'](surveys)
        self.assertEqual(expected, actual)    

    def test_transaction_amount_empty(self):
        surveys = []
        expected = 0
        actual = vars(statistics)['__transaction_amount'](surveys)
        self.assertEqual(expected, actual)

    def test_transaction_amount_many(self):
        surveys = [Survey(price=100) for _ in range(100)]
        expected = 100*100
        actual = vars(statistics)['__transaction_amount'](surveys)
        self.assertEqual(expected, actual)

    def test_transaction_amount(self):
        surveys = [Survey(price=100), Survey(price=50), Survey(price=30)]
        expected = sum([100, 50, 30])
        actual = vars(statistics)['__transaction_amount'](surveys)
        self.assertEqual(expected, actual)   

    def test_average_transaction_time_successful_transaction_empty(self):
        survey_listings = []
        expected = 0
        actual = vars(statistics)['__average_time_successful_transaction'](survey_listings)
        self.assertEqual(expected, actual)

    def test_average_transaction_time_successful_transaction(self):
        now = timedelta(days=100)
        created = timedelta(days=0)
        survey_listings = [ (Survey(time_submitted=now), Listing(created=created)) ]
        expected = 100
        actual = vars(statistics)['__average_time_successful_transaction'](survey_listings)
        self.assertEqual(expected, actual)

    def test_average_transaction_time_successful_transaction_many(self):
        survey_listings = [ 
            (Survey(time_submitted=timedelta(days=1)), Listing(created=timedelta(days=0))),
            (Survey(time_submitted=timedelta(days=2)), Listing(created=timedelta(days=0))),
            (Survey(time_submitted=timedelta(days=3)), Listing(created=timedelta(days=0))),
            (Survey(time_submitted=timedelta(days=4)), Listing(created=timedelta(days=0))),
            (Survey(time_submitted=timedelta(days=5)), Listing(created=timedelta(days=0))),
            (Survey(time_submitted=timedelta(days=6)), Listing(created=timedelta(days=0))),
            (Survey(time_submitted=timedelta(days=7)), Listing(created=timedelta(days=0))),
            (Survey(time_submitted=timedelta(days=8)), Listing(created=timedelta(days=0))),
            ]
        expected = sum([1,2,3,4,5,6,7,8])/8
        actual = vars(statistics)['__average_time_successful_transaction'](survey_listings)
        self.assertEqual(expected, actual)

    def test_listing_transaction_success_rate(self):
        buyer_surveys = []
        seller_surveys = []
        buyer_listings = []
        seller_listings = []
        expected_bsr = 100
        expected_ssr = 100
        expected_tsr = 100
        actual_bsr, actual_ssr, actual_tsr = \
            vars(statistics)['__listing_transaction_success_rate'] \
            (buyer_surveys, seller_surveys, buyer_listings, seller_listings)
        self.assertEqual(expected_bsr, actual_bsr)
        self.assertEqual(expected_ssr, actual_ssr)
        self.assertEqual(expected_tsr, actual_tsr)

    def test_listing_transaction_success_rate_buyer(self):
        buyer_surveys = [Survey()]
        seller_surveys = []
        buyer_listings = [Listing()]
        seller_listings = [Listing()]
        expected_bsr = 100
        expected_ssr = 0
        expected_tsr = 50
        actual_bsr, actual_ssr, actual_tsr = \
            vars(statistics)['__listing_transaction_success_rate'] \
            (buyer_surveys, seller_surveys, buyer_listings, seller_listings)
        self.assertEqual(expected_bsr, actual_bsr)
        self.assertEqual(expected_ssr, actual_ssr)
        self.assertEqual(expected_tsr, actual_tsr)

    def test_listing_transaction_success_rate_seller(self):
        buyer_surveys = []
        seller_surveys = [Survey(), Survey()]
        buyer_listings = [Listing(), Listing(), Listing()]
        seller_listings = [Listing(), Listing(), Listing(), Listing()]
        expected_bsr = 0
        expected_ssr = 50
        expected_tsr = 2.0/7.0*100
        actual_bsr, actual_ssr, actual_tsr = \
            vars(statistics)['__listing_transaction_success_rate'] \
            (buyer_surveys, seller_surveys, buyer_listings, seller_listings)
        self.assertEqual(expected_bsr, actual_bsr)
        self.assertEqual(expected_ssr, actual_ssr)
        self.assertAlmostEqual(expected_tsr, actual_tsr, delta=0.0001)

    def test_listing_transaction_success_rate_perfect(self):
        buyer_surveys = [Survey()]
        seller_surveys = [Survey()]
        buyer_listings = [Listing()]
        seller_listings = [Listing()]
        expected_bsr = 100
        expected_ssr = 100
        expected_tsr = 100
        actual_bsr, actual_ssr, actual_tsr = \
            vars(statistics)['__listing_transaction_success_rate'] \
            (buyer_surveys, seller_surveys, buyer_listings, seller_listings)
        self.assertEqual(expected_bsr, actual_bsr)
        self.assertEqual(expected_ssr, actual_ssr)
        self.assertEqual(expected_tsr, actual_tsr)











