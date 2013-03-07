from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
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
    
    def __unicode__(self):
        return self.title

    def isExpired(self):
        return self.expires <= timezone.now()

    def getDateCreated(self):
        return self.created
    
    def getLastModified(self):
        return self.lastModified
    
    def markModified(self):
        self.lastModified = timezone.now()
        
    
