import uuid
import datetime
import os
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms



CATEGORIES = ['Woods', 'Bricks', 'Shingles', 'Drywall', 'Toilets', 'Sinks',
                'Tubs', 'Windows', 'Doors', 'Fixtures', 'Cable and Wiring', 
                'Particle board', 'Cardboard', 'Cabinetry', 'Scrap metal',
                'Appliances', 'Other']
CITIES = ['Abbotsford', 'Burnaby', 'Chilliwack',
             'Coquitlam', 'Delta', 'Hope', 'Langley', 'Maple Ridge',
             'Mission', 'New Westminster', 'North Vancouver', 'Pitt Meadows',
             'Port Coquitlam', 'Port Moody', 'Richmond', 'Squamish', 'Surrey',
             'Vancouver', 'West Vancouver', 'White Rock', 'Whistler']

SALE_CHOICES=(("sell", 'Items for sale'), ("want", 'Items wanted'))
CAT_CHOICES = [(category, category) for category in CATEGORIES]
CITY_CHOICES = [(city, city) for city in CITIES]


class Listing(models.Model):
    
    for_sale = models.CharField(max_length=4, choices=SALE_CHOICES, default=SALE_CHOICES[0][0])
    url = models.CharField(max_length=110)
    creator = models.EmailField("creators email")
    created = models.DateTimeField("date created", auto_now_add=True)
    last_modified = models.DateTimeField("last modified", auto_now=True)
    title = models.CharField(max_length=100)
    text_content = models.TextField()
    verified = models.BooleanField(default=False)
    category = models.CharField(max_length=20, choices=CAT_CHOICES, default=CAT_CHOICES[0][0])
    price = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=30, choices=CITY_CHOICES, default='Vancouver')
    flag_count = models.SmallIntegerField("flag count", default=0)
    expires = models.DateTimeField("expiry date", 
        default=(timezone.now() + datetime.timedelta(days=30)), editable=True)
    expired = models.BooleanField(default=False)
    survey_time_sent = models.DateTimeField("survey time sent", blank=True, 
        null=True)
    uuid = models.CharField(max_length=36, default=uuid.uuid4)

    def mark_verified(self):
        self.verified = True
    
    def is_verified(self):
        return self.verified
   
   
    def __unicode__(self):
        return 'creator: %s, created: %s, title: %s, text_content: %s' \
            % (self.creator, self.created, self.title, self.text_content)

    def mark_modified(self):
        self.last_modified = timezone.now()

    def flag(self):
        self.flag_count + 1

    def is_expired(self):
        return self.expires <= timezone.now()
    
    def renew(self):
        self.save()

    def get_type(self):
        return self.type
     
    def set_type(self, t):
        self.type = t
        
    def set_url(self, u):
        self.url = u
        
    def get_url(self):
        return self.url
    
    def get_creator(self):
        return self.creator
    
    def get_created_time(self):
        return self.created

    def get_last_modified_time(self):
        return self.last_modified

    def get_title(self):
        return self.title
    
    def set_title(self, t):
        self.title = t

    def get_text_content(self):
        return self.text_content
    
    def set_text_content(self, t):
        self.text_content = t
    
    def increment_flags(self):
        self.flag_count += 1
    
    def get_flag_count(self):
        return self.flag_count
    
    def get_uuid(self):
        return self.uuid
    
    def get_city(self):
        return self.city
    
def get_listings_categories():
    return CAT_CHOICES

def get_sale_categories():
    return SALE_CHOICES

def get_city_categories():
    return CITY_CHOICES


class ListingForm(ModelForm):
    creator = forms.EmailField(required = True)
    email_verification = forms.EmailField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['creator'].label = "Email address"
        self.fields['email_verification'].label = "Verify email"
        self.fields['address'].label = "Address"
        self.fields['city'].label = "City"
        self.fields['text_content'].label = "Description"
        self.fields['for_sale'].label = "Type of listing"
        # setting attribute names for css
        self.fields['address'].widget.attrs.update({'id' : 'detail_address'})
        self.fields['city'].widget.attrs.update({'id' : 'detail_city'})
        self.fields['text_content'].widget.attrs.update({'id' : 'detail_text_content'})
        self.fields['for_sale'].widget.attrs.update({'id' : 'detail_type'})

    
    class Meta:
        model = Listing
        #exclude = ['url', 'verified', 'flag_count']
        fields = ['creator', 'email_verification', 'title','for_sale','category', 'price', 'address', 'city', 'text_content']
        
        
    def clean(self):
        cleaned_data = self.cleaned_data
        creator_email = cleaned_data.get('creator')
        verified_email = cleaned_data.get('email_verification')
        category = cleaned_data.get('category')
        type = cleaned_data.get('type')
        
        if creator_email != verified_email:
            self._errors["email_verification"] = self.error_class(["The email and verification entered do not match"])
        if not category:
            self._errors["category"] = self.error_class(["You must choose category"])
    
        return cleaned_data
    
    def get_type(self):
        return "ListingForm"
        
class EditListingForm(ModelForm):
    class Meta:
        model = Listing

        #exclude = ['flag_count', 'verified','type', 'url', 'uuid','creator']
        fields = ['title', 'for_sale', 'category', 'price', 'address', 'city', 'text_content']
           
    def get_type(self):
        return "EditListingForm"

        
# PhotoStroage model
class Photo(models.Model):
   listing = models.ForeignKey(Listing)
   photo =  models.ImageField(upload_to='photos/listings/%Y/%B/%d/')
   caption = models.CharField(max_length=200)
   
   def imagename(self):
       return os.path.basename(self.photo.name)
   
class PostPictures(models.Model):
   postid = models.IntegerField() 
   photo =  models.ImageField(upload_to='photos/%Y/%B/%d/')
   
class UploadForm(forms.Form):
        picture  = forms.ImageField(label='Add a picture:',)
        
        
        
