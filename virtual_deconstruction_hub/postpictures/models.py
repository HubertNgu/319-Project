from django.db import models
from django import forms

class PostPictures(models.Model):
   postid = models.IntegerField() 
   photo =  models.ImageField(upload_to='photos/%Y/%B/%d/')
   
class UploadForm(forms.Form):
        picture  = forms.ImageField(label='Select a file',)

