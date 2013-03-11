from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length = 20)
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    phoneno = models.CharField(max_length = 10)
    address = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    country = models.CharField(max_length = 50)
    province = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    isverified = models.BooleanField(default = 0)

def __unicode__(self):
        return self.name