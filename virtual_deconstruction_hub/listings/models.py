import uuid
import datetime

from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms

WOOD = 'wood'
BRICKS = 'bricks'
SHINGL = 'shingl'
DRYWAL = 'drywal'
TOILET = 'toilet'
SINKS = 'sinks'
TUBS = 'tubs'
WINDOW = 'window'
DOORS = 'doors'
FIXTUR = 'fixtur'
CABWIR = 'cabWir'
PARTBD = 'partBd' 
CARDBD = 'cardBd'
SCRAPM = 'scrapM'
CABINT = 'cabint'
APPLIA = 'applian'
OTHER = 'other'
CAT_CHOICES = ((WOOD, "Woods"), (BRICKS, "Bricks"), (SHINGL, "Shingles"),
    (DRYWAL, "Drywall"), (TOILET, "Toilets"), (SINKS, "Sinks"),
    (TUBS, "Tubs"), (WINDOW, "Windows"), (DOORS, "Doors"),(FIXTUR, "Fixtures"),
    (CABWIR, "Cable and Wiring"), (PARTBD, "Particle board"), (CARDBD, "Cardboard"),
    (CABINT, "Cabinetry"), (SCRAPM, "Scrap metal"), (APPLIA, "Appliances"), (OTHER, "Other"),)



class Listing(models.Model):
    
    for_sale = models.BooleanField()
    url = models.CharField(max_length=110)
    creator = models.EmailField("creators email")
    created = models.DateTimeField("date created", auto_now_add=True)
    lastModified = models.DateTimeField("last modified", auto_now=True)
    title = models.CharField(max_length=100)
    textContent = models.TextField()
    verified = models.BooleanField(default=False)
    category = models.CharField(max_length=20, choices = CAT_CHOICES, default = WOOD)
    price = models.CharField(max_length=20, blank=True)
    num = models.IntegerField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = 'British Columbia'
    zipcode = models.CharField(max_length=6)
    location = models.CharField(max_length=100, blank=True)
    flagCount = models.SmallIntegerField("flag count", default=0)
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
        return 'creator: %s, created: %s, title: %s, textContent: %s' \
            % (self.creator, self.created, self.title, self.textContent)

    def markModified(self):
        self.lastModified = timezone.now()

    def flag(self):
        self.flagCount + 1

    def isExpired(self):
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

class ListingForm(ModelForm):
    
    email_verification = forms.EmailField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['creator'].label = "Email address"
        self.fields['email_verification'].label = "Verify email"
        self.fields['num'].label = "Street Number"
        self.fields['street'].label = "Street Name"
        self.fields['city'].label = "City"
        self.fields['zipcode'].label = "Postal code"
        self.fields['textContent'].label = "Description"
        
    
    class Meta:
        model = Listing
        exclude = ['url', 'verified', 'flagCount']
        fields = ['creator', 'email_verification', 'title','category', 'price', 'num', 
                  'street', 'city', 'zipcode', 'textContent']
        
        
    def clean(self):
        cleaned_data = self.cleaned_data
        creator_email = cleaned_data.get('creator')
        verified_email = cleaned_data.get('email_verification')
        category = cleaned_data.get('category')
        zipcode = cleaned_data.get('zipcode')
        
        if creator_email != verified_email:
            self._errors["email_verification"] = self.error_class(["The email and verification entered do not match"])
        if not category:
            self._errors["category"] = self.error_class(["You must choose category"])
    
        return cleaned_data
        
class EditListingForm(ModelForm):
    class Meta:
        model = Listing
        #exclude = ['flag_count', 'verified','type', 'url', 'uuid','creator']
        fields = ['title', 'category', 'price', 'num', 'street', 'city', 'zipcode', 'textContent']

# PhotoStroage model
class Photo(models.Model):
   listing = models.ForeignKey(Listing)
   photo =  models.ImageField(upload_to='photos/listings/%Y/%B/%d/')
   caption = models.CharField(max_length=200)
   
   def imagename(self):
       return os.path.basename(self.photo.name)
   


            
        
        
        
