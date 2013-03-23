from django.db import models
from django import forms
from django.forms import ModelForm
import uuid
import os
from django.conf import settings

TIME_ZONE = settings.TIME_ZONE

# Create your models here.
class Post(models.Model):
    url = models.CharField(max_length=110)
    creator = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    text_content = models.TextField()
    verified = models.BooleanField(default=False)
    flag_count = models.SmallIntegerField(default=0)
    #type must be one of "blog", "user" or "proj"
    PROJ = "proj"
    STORY = "stry"
    BLOG = "blog"
    TYPE_CHOICES = ((PROJ, "Project Idea"),
                    (STORY, "Success Story"),
                    (BLOG, "Blog Post"))
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, default=PROJ)
    uuid = models.CharField(max_length=36, default=uuid.uuid4)
    
    def mark_verified(self):
        self.verified = True
        
    def is_verified(self):
        return self.verified
    
    def __unicode__(self):
        return self.title
    
    def renew(self):
        self.save()

    def get_type(self):
        return self.type
     
    def set_type(self, t):
        self.type = t
        
    def set_url(self, u):
        self.url = u
        
    def get_url(self):
        return self.url
    
    def get_creator(self):
        return self.creator
    
    def get_created_time(self):
        return self.created

    def get_last_modified_time(self):
        return self.last_modified

    def get_title(self):
        return self.title
    
    def set_title(self, t):
        self.title = t

    def get_text_content(self):
        return self.text_content
    
    def set_text_content(self, t):
        self.text_content = t
    
    def increment_flags(self):
        self.flag_count += 1
    
    def get_flag_count(self):
        return self.flag_count
    
    def get_uuid(self):
        return self.uuid
    
# Create the form class.
class PostForm(ModelForm):
    creator = forms.EmailField(required=True)
    email_verification = forms.EmailField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs) 
        self.fields['creator'].label = "Email address"
        self.fields['email_verification'].label = "Verify email"

    class Meta:
        model = Post
        #sets hidden attributes that we don't want individual users filling out
        #exclude = ['flag_count', 'verified','type', 'url', 'uuid']
        #sets the order in which fields displayed when form rendered
        fields = ['creator', 'email_verification', 'title', 'text_content']
        
    def clean(self):
        cleaned_data = self.cleaned_data
        creator_email = cleaned_data.get("creator")
        verified_email = cleaned_data.get("email_verification")

        if creator_email != verified_email:
            self._errors["email_verification"] = self.error_class(["The email and verification entered do not match."])

        # Always return the full collection of cleaned data.
        return cleaned_data

class EditPostForm(ModelForm):
    class Meta:
        model = Post
        #exclude = ['flag_count', 'verified','type', 'url', 'uuid','creator']
        fields = ['title', 'text_content']
        
    
# PhotoStroage model
class Photo(models.Model):
   post = models.ForeignKey(Post)
   photo =  models.ImageField(upload_to='photos/posts/%Y/%B/%d/')
   caption = models.CharField(max_length=200)
   
   def get_caption(self):
        return self.caption
   
   def get_url(self):
        return self.photo
   
   def imagename(self):
        return os.path.basename(self.photo.name)
   
class UploadForm(ModelForm):
    class Meta:
        model = Photo
        exclude = ['post']
        fields = ['photo', 'caption']
