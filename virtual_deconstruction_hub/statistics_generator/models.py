from django.db import models

class Statistics(models.Model):
	successful_transaction_amount = models.IntegerField()
	average_transaction_time = models.IntegerField()
	transaction_success_rate = models.FloatField()

class StatisticsCategory(models.Model):
	statistics_id = models.IntegerField()
	category = models.CharField(max_length=30)
	survey_count = models.IntegerField()
	buyer_count = models.IntegerField()
	seller_count = models.IntegerField()
	amount = models.IntegerField()