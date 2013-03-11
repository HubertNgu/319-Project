from django.db import models

class VerificationApp(models.Model):
    username = models.CharField(max_length = 50)
    verificationcode = models.CharField(max_length = 10)
    
