'''
 Survey models module. This module contains the database models for the
 Survey class and the SurveyForm class.

 @author Hubert Ngu
'''

from listings.models import Listing, CAT_CHOICES

from django.db import models
from django.forms import ModelForm, Textarea

# Fields included here will be visisble on the HTML page
FIELDS = ['listing_id', 'item', 'category', 'price', 'address', 
            'city', 'comments']

class Survey(models.Model):
    '''
    Survey model class. This represents a single tuple in the
    survey_system_survey table in the database.
    '''
    listing_id = models.IntegerField()
    item = models.CharField(max_length=30, blank=True)
    category = models.CharField(max_length=20, choices=CAT_CHOICES, default=CAT_CHOICES[0][0])
    price = models.FloatField()
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    comments = models.CharField(max_length=500, blank=True)
    time_submitted = models.DateTimeField("time submitted", auto_now_add=True)

class SurveyForm(ModelForm):
    '''
    Survey form class. This represents the form that will be dispalyed on
    the HTML survey.html page.
    '''
    def __init__(self, *args, **kwargs):
        '''
        Constructor for SurveyForm. Should pass in instance=Survey()
        and possibly for initial=dict() with key value pairs for initial
        values for the form fields.
        '''
        super(SurveyForm, self).__init__(*args, **kwargs)
        # Hide the listing_id field as it will be assigned a value automaticaly
        self.fields['listing_id'].widget = self.fields['listing_id'].hidden_widget()

        # Create the labels for the form fields based on the attributes of Survey
        # e.g. item will be labelled as Item
        for field in FIELDS:
            self.fields[field].label = field.capitalize().replace('_', ' ')

    def clean(self):
        '''
        Override the clean function to provide error messages for specific fields.
        '''
        for field in FIELDS:
            vars(self)[field] = self.cleaned_data.get(field)
    
        # Add error messages here for empty fields.
        if not self.fields['price']:
            self._errors['price'] = ['Please enter the total amount in CAD of the transaction']

        return self.cleaned_data

    # Meta class for the SurveyForm. Declare the model the ModelForm takes and
    # the visible fields in the form.
    class Meta:
        model = Survey
        fields = FIELDS

        # Add a widget for comments to expand the text area.
        widgets = {
            'comments': Textarea(attrs={'cols': 80, 'rows': 20}),
        }