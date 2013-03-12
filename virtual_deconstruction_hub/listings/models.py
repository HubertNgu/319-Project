from django.db import models
from django.utils import timezone
from django.forms import ModelForm
import datetime
import MySQLdb

class Listing(models.Model):
    
    creator = models.EmailField("creators email")
    created = models.DateTimeField("date created", auto_now_add=True)
    lastModified = models.DateTimeField("last modified", auto_now=True)
    expires = models.DateTimeField("expiry date", default=(timezone.now() + datetime.timedelta(days=30)), editable=True)
    title = models.CharField(max_length=100)
    textContent = models.TextField()
    photo1 = models.FileField(blank=True, upload_to='photos/%Y/%m/%d')
    photo2 = models.FileField(blank=True, upload_to='photos/%Y/%m/%d')
    photo3 = models.FileField(blank=True, upload_to='photos/%Y/%m/%d')
    photo4 = models.FileField(blank=True, upload_to='photos/%Y/%m/%d')
    verified = models.BooleanField(default=False)
    flagCount = models.SmallIntegerField("flag count", default=0)
    
    
#    def create_listing(self, creator, title, textContext, photo1, photo2, photo3, photo4):
#        listing = (creator=creator,
#                   created = timezone.now(),
#                   lastModified = timezone.now(),
#                   expires = timezone.now() + datetime.timedelta(days=30),
#                   title=title,
#                   textContext = textContext,
#                   photo1 = photo1,
#                   photo2 = photo2,
#                   photo3 = photo3,
#                   photo4 = photo4)
   
    def __unicode__(self):
        return self.title
    
    def getCreator(self):
        return self.creator

    def getDateCreated(self):
        return self.dateCreated

    def getLastModified(self):
        return self.lastModified

    def getFlagCount(self):
        return self.flagCount

    def markModified(self):
        self.lastModified = timezone.time()

    def flag(self):
        self.flagCount + 1

    def isExpired(self):
        return self.expires <= timezone.now()
    

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ('creator', 'title', 'textContent', 
                  'photo1', 'photo2', 'photo3', 'photo4')

    

            
        
        
        