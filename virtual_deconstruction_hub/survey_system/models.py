import uuid
import datetime

from listings.models import CAT_CHOICES
from django.db import models
from django.utils import timezone
from django.forms import ModelForm, Textarea

FIELDS = ['item', 'category', 'quantity', 'price', 'street_number', 'street_name',
	    		'city', 'postal_code', 'comments']

class Survey(models.Model):
	item = models.CharField(max_length=30)
	category = models.CharField(max_length=6, choices = CAT_CHOICES, default = CAT_CHOICES[0][0])
	quantity = models.IntegerField()
	price = models.FloatField()
	street_number = models.IntegerField()
	street_name = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=6)
	comments = models.CharField(max_length=500)
	listing_id = models.IntegerField()
	time_submitted = models.DateTimeField("time submitted", auto_now_add=True)

class SurveyForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(SurveyForm, self).__init__(*args, **kwargs)
		for field in FIELDS:
			self.fields[field].label = field.capitalize().replace('_', ' ')

	def clean(self):
		for field in FIELDS:
			vars(self)[field] = self.cleaned_data.get(field)
		
		for field in FIELDS:
			if not vars(self)[field]:
				self._errors[field] = self.error_class(['Please specifiy the %s' % field])

		return self.cleaned_data

	class Meta:
		model = Survey
		exclude = ['listing_id', 'time_submitted']
		fields = FIELDS

		widgets = {
            'comments': Textarea(attrs={'cols': 80, 'rows': 20}),
        }