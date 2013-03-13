from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    creator = models.EmailField("creators email")
    created = models.DateTimeField("date created", auto_now_add=True)
    last_modified = models.DateTimeField("last modified", auto_now=True)
    title = models.CharField(max_length=100)
    text_content = models.TextField()
    photo1 = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d')
    photo2 = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d')
    photo3 = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d')
    photo4 = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d')
    verified = models.BooleanField(default=False)
    flag_count = models.SmallIntegerField("flag count", default=0)
    #type must be one of "blog", "user" or "proj"
    PROJ = "PROJ"
    USER = "USER"
    BLOG = "BLOG"
    TYPE_CHOICES = ((PROJ, "Project Idea"),
                    (USER, "User Story"),
                    (BLOG, "Blog Post"))
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, default=PROJ)
    
    def mark_verified(self):
        self.verified = True
        
    def is_verfied(self):
        return self.verified
    
    def __unicode__(self):
        return self.title
    
    def getType(self):
        return self.type
    
    def setType(self, t):
        self.type = t
    
    
    
