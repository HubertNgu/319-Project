from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms
import datetime



class Listing(models.Model):
    
    url = models.CharField(max_length=110)
    creator = models.EmailField("creators email")
    created = models.DateTimeField("date created", auto_now_add=True)
    lastModified = models.DateTimeField("last modified", auto_now=True)
    expires = models.DateTimeField("expiry date", default=(timezone.now() + datetime.timedelta(days=30)), editable=True)
    title = models.CharField(max_length=100)
    textContent = models.TextField()
    verified = models.BooleanField(default=False)
    flagCount = models.SmallIntegerField("flag count", default=0)
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
    category = models.CharField(max_length=6, choices = CAT_CHOICES, default = WOOD)
    price = models.CharField(max_length=20, blank=True)
    num = models.IntegerField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = 'British Columbia'
    zipcode = models.CharField(max_length=6)
    

   
    def __unicode__(self):
        return 'creator: %s, created: %s, title: %s, textContent: %s' \
            % (self.creator, self.created, self.title, self.textContent)

    def markModified(self):
        self.lastModified = timezone.now()

    def flag(self):
        self.flagCount + 1

    def isExpired(self):
        return self.expires <= timezone.now()
    



class ListingForm(ModelForm):
    email_verification = forms.EmailField(required=True)
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
        if creator_email != verified_email:
            self._errors["email_verification"] = self.error_class(["The email and verification entered do not match"])
        if not category:
            self._errors["category"] = self.error_class(["You must choose category"])
        return cleaned_data

    

            
        
        
        