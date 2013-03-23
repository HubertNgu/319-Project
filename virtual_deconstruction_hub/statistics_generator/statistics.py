'''
 Statistics module responsible for generating statistics based on the
 listings and surveys in the database.

 @author Hubert Ngu
 @author Jason Hou
'''

import logging
from survey_system.models import Survey
from listings.models import Listing, CAT_CHOICES
from statistics_generator.models import Statistics, StatisticsCategory

from util import ValueCounter
from collections import Counter

logger = logging.getLogger(__name__)

def __category_rank(category_list):
	'''
	Returns of map of category to count pairs for all surveys submitted.
	'''
	return Counter([element.category for element in category_list])

def __survey_category_transaction_amount(surveys):
	'''
	Returns a map of category to amount pairs for all surveys submitted.
	'''
	amounts = ValueCounter.ValueCounter()
	for survey in surveys:
		amounts.update(survey.category, survey.price)
	return amounts

def __survey_average_transaction_amount(surveys):
	'''
	Returns the average amount of money paid in all transactions.
	'''
	return float(sum([survey.price for survey in surveys])) / \
		float(len(surveys)) if len(surveys) > 0 else 0

def __transaction_amount(surveys):
	'''
	Returns the total amount of money paid in all transactions.
	'''
	return float(sum([survey.price for survey in surveys]))

def __average_time_successful_transaction(survey_listings):
	'''
	Returns the average time for a transaction to complete.
	'''
	transaction_times = list()
	for survey, listing in survey_listings:
		transaction_times.append((listing.created - survey.time_submitted).seconds)
	return sum(transaction_times) / len(transaction_times) \
			if len(transaction_times) > 0 else 0
			
def __listing_transaction_success_rate(buyer_surveys, seller_surveys, 
		buyer_listings, seller_listings):
	'''
	Returns the success rate for buyer transactions, seller_transactions,
	and all transactions.
	'''
	buyer_success_rate = 100*float(len(buyer_surveys)) / float(len(buyer_listings)) \
		if len(buyer_listings) > 0 else 0
	seller_success_rate = 100*float(len(seller_surveys)) / float(len(seller_listings)) \
		if len(seller_listings) > 0 else 0
	total_success_rate = 100*float(len(buyer_surveys) + len(seller_surveys)) / \
			float((len(buyer_listings) + len(seller_listings))) \
			if len(buyer_listings) + len(seller_listings) > 0 else 0
	return buyer_success_rate, seller_success_rate, total_success_rate

def generate_statistics():
	'''
	Generates statistics and adds a new tuple in the 
	statistics_generator_statistics table.
	'''
	surveys = Survey.objects.all()
	listings = Listing.objects.all()
	buyer_listings = Listing.objects.filter(for_sale='want')
	seller_listings = Listing.objects.filter(for_sale='sell')
	survey_listings = [(survey, Listing.objects.get(id=survey.listing_id)) for survey in surveys]
	buyer_surveys = [survey for survey, listing in survey_listings if listing.for_sale == 'want']
	seller_surveys = [survey for survey, listing in survey_listings if listing.for_sale == 'sell']
	logger.info('Successfully gathered all data from database used for generating statistics')

	# Maps of category data
	survey_category_rank_stats = __category_rank(surveys)
	buyer_category_rank_stats = __category_rank(buyer_listings)
	seller_category_rank_stats = __category_rank(seller_listings)
	survey_category_transaction_amount_stats = \
		__survey_category_transaction_amount(surveys)
	logger.info('Successfully generated category statistics')

	# Integer data values
	average_transaction_amount = __survey_average_transaction_amount(surveys)
	logger.info('Successfully generated average transaction amount statistics')

	buyer_transaction_amount = __transaction_amount(buyer_surveys)
	logger.info('Successfully generated buyer transaction amount statistics')

	seller_transaction_amount = __transaction_amount(seller_surveys)
	logger.info('Successfully generated seller transaction amount statistics')

	successful_transaction_amount = __transaction_amount(surveys)
	logger.info('Successfully generated survey transaction amount statistics')

	average_transaction_time = __average_time_successful_transaction(survey_listings)
	logger.info('Successfully generated average transaction time statistics')

	buyer_transaction_success_rate, seller_transaction_success_rate, \
		total_transaction_success_rate  = __listing_transaction_success_rate(
			buyer_surveys, seller_surveys,
			buyer_listings, seller_listings)
	logger.info('Successfully generated transaction success rate statistics')

	# Create the Statistics tuple and save it.
	statistics = Statistics(number_surveys=len(surveys),
					number_listings=len(listings),
					number_buyer_surveys=len(buyer_surveys),
					number_seller_surveys=len(seller_surveys),
					number_buyer_listings=len(buyer_listings),
					number_seller_listings=len(seller_listings),
					average_transaction_amount=average_transaction_amount,
					buyer_transaction_amount=buyer_transaction_amount,
					seller_transaction_amount=seller_transaction_amount,
					successful_transaction_amount=successful_transaction_amount,
					average_transaction_time=average_transaction_time,
					buyer_transaction_success_rate=buyer_transaction_success_rate,
					seller_transaction_success_rate=seller_transaction_success_rate,
					total_transaction_success_rate=total_transaction_success_rate)
	statistics.save()

	# Create the StatisticsCategory tuples and save them.
	for name, category in CAT_CHOICES:
		statistics_category = \
			StatisticsCategory(statistics_id=statistics.id, 
				category=category, 
				survey_count=survey_category_rank_stats[category], 
				buyer_count=buyer_category_rank_stats[category],
				seller_count=seller_category_rank_stats[category], 
				amount=survey_category_transaction_amount_stats.get(category))
		statistics_category.save()

	logger.info('Successfully save generated statistics to the database')	












