from django.db import models
from django.utils import timezone
import datetime
import MySQLdb

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

    def getCreator(self):
        return self.creator
    
    def getDateCreated(self):
        return self.dateCreated
    
    def getLastModified(self):
        return self.lastModified
    
    def getFlagCount(self):
        return self.flagCount
    
    def markModified(self, ntitle, ncontent, nphoto1, nphoto2, nphoto3, nphoto4):
        self.lastModified = time.time()
        self.title = ntitle
        self.textcontent = ncontent
        self.photo1 = nphoto1
        self.photo2 = nphoto2
        self.photo3 = nphoto3
        self.photo4 = nphoto4
    
#    def renderMultiple(listings):
#        for l in listings:
#            print l.title
#            print l.creator
#            print l.created

               
#    def renderSingle(self):
  
    def search(keyword):
        results = Listings.objects.raw('SELECT * FROM listings WHERE title LIKE %%s%', [keyword])
        return results
        
    def flag(self):
        self.flagCount + 1
    
    def isExpired(self):
        return self.expires <= timezone.now()


            
        
        
        