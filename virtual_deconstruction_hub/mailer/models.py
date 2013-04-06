from django.db import models

# Create your models here.
class Email(models.Model):
	to_email = models.CharField(max_length=200)
	from_email = models.CharField(max_length=200)
	subject = models.CharField(max_length=200)
	message = models.CharField(max_length=1000)
	email_type = models.IntegerField(default=0)
	send_date = models.DateTimeField(auto_now=True)
