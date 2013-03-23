'''
 Statistics models module. This module contains the database models for the
 Statistics class and the StatisticsCategory class.

 @author Hubert Ngu
 @author Jason Hou
'''

from django.db import models

class Statistics(models.Model):
	'''
	Statistics model class. This represents a single tuple in the
	statitics_generator_statistics table in the database.
	'''
	number_surveys = models.IntegerField()
	number_listings = models.IntegerField()
	number_buyer_surveys = models.IntegerField()
	number_seller_surveys = models.IntegerField()
	number_buyer_listings = models.IntegerField()
	number_seller_listings = models.IntegerField()
	average_transaction_amount = models.FloatField()
	buyer_transaction_amount = models.FloatField()
	seller_transaction_amount = models.FloatField()
	successful_transaction_amount = models.FloatField()
	average_transaction_time = models.IntegerField()
	buyer_transaction_success_rate = models.FloatField()
	seller_transaction_success_rate = models.FloatField()
	total_transaction_success_rate = models.FloatField()

class StatisticsCategory(models.Model):
	'''
	StatisticsCategory model class. This represents a single tuple in the
	statitics_generator_statisticscategory table in the database.
	'''
	statistics_id = models.IntegerField()
	category = models.CharField(max_length=30)
	survey_count = models.IntegerField()
	buyer_count = models.IntegerField()
	seller_count = models.IntegerField()
	amount = models.IntegerField()