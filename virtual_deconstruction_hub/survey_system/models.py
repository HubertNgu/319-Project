import uuid
import datetime
from listings.models import Listing, CAT_CHOICES

from django.db import models
from django.utils import timezone
from django.forms import ModelForm, Textarea, IntegerField

FIELDS = ['listing_id', 'item', 'category', 'price', 'address', 'city', 'comments']

class Survey(models.Model):
    listing_id = models.IntegerField()
    item = models.CharField(max_length=30, blank=True)
    category = models.CharField(max_length=20, choices=CAT_CHOICES, default=CAT_CHOICES[0][0])
    price = models.FloatField()
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    comments = models.CharField(max_length=500, blank=True)
    time_submitted = models.DateTimeField("time submitted", auto_now_add=True)

class SurveyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.fields['listing_id'].widget = self.fields['listing_id'].hidden_widget()
        for field in FIELDS:
            self.fields[field].label = field.capitalize().replace('_', ' ')

    def clean(self):
        for field in FIELDS:
            vars(self)[field] = self.cleaned_data.get(field)
    
        if not self.fields['price']:
            self._errors['price'] = ['Please enter the total amount in CAD of the transaction']

        return self.cleaned_data

    class Meta:
        model = Survey
        fields = FIELDS

        widgets = {
            'comments': Textarea(attrs={'cols': 80, 'rows': 20}),
        }