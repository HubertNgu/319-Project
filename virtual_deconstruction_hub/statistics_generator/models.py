from django.db import models

class Statistics(models.Model):
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
	statistics_id = models.IntegerField()
	category = models.CharField(max_length=30)
	survey_count = models.IntegerField()
	buyer_count = models.IntegerField()
	seller_count = models.IntegerField()
	amount = models.IntegerField()

class StatisticsLocation(models.Model):
	statistics_id = models.IntegerField()
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=30)
	postal_code = models.CharField(max_length=6)