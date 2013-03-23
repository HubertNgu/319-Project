from django.db import models

class User(models.Model):
    username = models.CharField(max_length = 20)
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    phoneno = models.CharField(max_length = 10)
    password = models.CharField(max_length = 20)
    signupdate = models.DateTimeField('signupdate')
    lastloggedindate = models.DateTimeField('lastloggedindate')
    role = models.IntegerField('role')
    profileid = models.IntegerField('profileid')
    isverified = models.BooleanField(default = 0)
    
