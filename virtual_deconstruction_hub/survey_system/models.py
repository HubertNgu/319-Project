from django.db import models

class Survey(models.Model):
	item = models.CharField(max_length = 30)
	quantity = models.IntegerField()
	price = models.FloatField()
	comments = models.CharField(max_length = 500)

	def __unicode__(self):
		return 'item: %s, quantity: %s, price: %s, comments: %s' \
			% (item, quantity, price, comments)