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

def survey_average_transaction_amount(surveys):
	return float(sum([survey.price for survey in surveys])) / \
		float(len(surveys)) if len(surveys) > 0 else 0

def buyer_transaction_total_amount(buyer_surveys):
	return float(sum([survey.price for survey in buyer_surveys]))

def seller_transaction_total_amount(seller_surveys):
	return float(sum([survey.price for survey in seller_surveys]))

def survey_transaction_total_amount(surveys):
	return sum([survey.price for survey in surveys])

def average_time_successful_transaction(survey_listings):
	transaction_times = list()
	for survey, listing in survey_listings:
		transaction_times.append((listing.created - survey.time_submitted).seconds)
	return sum(transaction_times) / len(transaction_times) \
			if len(transaction_times) > 0 else 0
			
def listing_transaction_success_rate(buyer_surveys, seller_surveys, 
		buyer_listings, seller_listings):
	buyer_success_rate = 100*float(len(buyer_surveys)) / float(len(buyer_listings)) \
		if len(buyer_listings) > 0 else 0
	seller_success_rate = 100*float(len(seller_surveys)) / float(len(seller_listings)) \
		if len(seller_listings) > 0 else 0
	total_success_rate = 100*float(len(buyer_surveys) + len(seller_surveys)) / \
			float((len(buyer_listings) + len(seller_listings))) \
			if len(buyer_listings) + len(seller_listings) > 0 else 0

	return buyer_success_rate, seller_success_rate, total_success_rate

def generate_statistics():
	surveys = Survey.objects.all()
	listings = Listing.objects.all()
	buyer_listings = Listing.objects.filter(for_sale='want')
	seller_listings = Listing.objects.filter(for_sale='sell')
	survey_listings = [(survey, Listing.objects.get(id=survey.listing_id))
						for survey in surveys]
	buyer_surveys = [survey for survey, listing in survey_listings if not listing.for_sale]
	seller_surveys = [survey for survey, listing in survey_listings if listing.for_sale]

	# Maps of category data
	survey_category_rank_stats = survey_category_rank(surveys)
	buyer_category_rank_stats = buyer_category_rank(buyer_listings)
	seller_category_rank_stats = seller_category_rank(seller_listings)
	survey_category_transaction_amount_stats = \
		survey_category_transaction_amount(surveys)

	# Integer data values
	average_transaction_amount = survey_average_transaction_amount(surveys)
	buyer_transaction_amount = buyer_transaction_total_amount(buyer_surveys)
	seller_transaction_amount = seller_transaction_total_amount(seller_surveys)
	successful_transaction_amount = survey_transaction_total_amount(surveys)
	average_transaction_time = average_time_successful_transaction(survey_listings)
	buyer_transaction_success_rate, seller_transaction_success_rate, \
		total_transaction_success_rate  = listing_transaction_success_rate(
			buyer_surveys, seller_surveys,
			buyer_listings, seller_listings)

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

	for name, category in CAT_CHOICES:
		statistics_category = \
			StatisticsCategory(statistics_id=statistics.id, 
				category=category, 
				survey_count=survey_category_rank_stats[category], 
				buyer_count=buyer_category_rank_stats[category],
				seller_count=seller_category_rank_stats[category], 
				amount=survey_category_transaction_amount_stats.get(category))
		statistics_category.save()












