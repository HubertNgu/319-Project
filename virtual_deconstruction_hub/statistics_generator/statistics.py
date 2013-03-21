# Statistics Class
from survey_system.models import Survey
from listings.models import Listing, CAT_CHOICES
from statistics_generator.models import Statistics, StatisticsCategory

from util import ValueCounter
from collections import Counter

def survey_category_rank(surveys):
	return Counter([survey.category for survey in surveys])

def buyer_category_rank(buyer_listings):
	return Counter([listing.category for listing in buyer_listings])

def seller_category_rank(seller_listing):
	return Counter([listing.category for listing in seller_listing])

def survey_category_transaction_amount(surveys):
	amounts = ValueCounter.ValueCounter()
	for survey in surveys:
		amounts.update(survey.category, survey.price)
	return amounts

def survey_transaction_total_amount(surveys):
	return sum([survey.price for survey in surveys])

def average_time_successful_transaction(survey_listings):
	transaction_times = list()
	for survey, listing in survey_listings.items():
		transaction_times.append((listing.created - survey.time_submitted).seconds)
	return sum(transaction_times) / len(transaction_times) \
			if len(transaction_times) > 0 else 0
			
		
		
def listing_transaction_success_rate(survey_listings, buyer_listings, seller_listings):
	buyers, sellers = list(), list()
	for survey, listing in survey_listings:
		if listing.type == 'buyer':
			buyers.append(survey)
		else:
			sellers.append(survey)

	return len(buyers) / len(buyer_listings), len(sellers) / len(seller_listings)

def generate_statistics():
	surveys = Survey.objects.all()
	#buyer_listings = Listing.objects.get(type=='buyer')
	#seller_listings = Listing.objects.get(type=='seller')
	survey_listings = {survey : Listing.objects.get(id=survey.listing_id) for survey in surveys}

	# Maps of category data
	survey_category_rank_stats = survey_category_rank(surveys)
	#buyer_category_rank_stats = buyer_category_rank(buyer_listings)
	#seller_category_rank_stats = seller_category_rank(seller_listings)
	survey_category_transaction_amount_stats = \
		survey_category_transaction_amount(surveys)

	# Integer data values
	successful_transaction_amount = survey_transaction_total_amount(surveys)
	average_transaction_time = average_time_successful_transaction(survey_listings)
	#transaction_success_rate = listing_transaction_success_rate(survey_listings, 
	#		buyer_listings, seller_listings)

	statistics = Statistics(successful_transaction_amount=successful_transaction_amount,
					average_transaction_time=average_transaction_time,
					transaction_success_rate=100)
	statistics.save()

	for name, category in CAT_CHOICES:
		statistics_category = \
			StatisticsCategory(statistics_id=statistics.id, 
				category=category, 
				survey_count=survey_category_rank_stats[category], 
				buyer_count=0,
				seller_count=0, 
				amount=survey_category_transaction_amount_stats.get(category))
		statistics_category.save()












