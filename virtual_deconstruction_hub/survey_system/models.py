import uuid
import datetime

from django.db import models
from django.utils import timezone

class Survey(models.Model):
	item = models.CharField(max_length = 30)
	category = models.CharField(max_length = 30)
	quantity = models.IntegerField()
	price = models.FloatField()
	location = models.CharField(max_length = 30)
	comments = models.CharField(max_length = 500)
	listing_id = models.IntegerField()
	time_submitted = models.DateTimeField("time submitted", auto_now_add=True)

	def __unicode__(self):
		return 'item: %s, category: %s, quantity: %s, price: %s, ' \
		' location: %s, comments: %s, listing_id: %s, time_submitted: %s' \
		% (item, category, quantity, price, location, comments, 
			listing_id, time_submitted)