from django.db import models
from django import forms
from django.forms import ModelForm


# Create your models here.
class Post(models.Model):
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
        
# Create the form class.
class PostForm(ModelForm):
    email_verification = forms.EmailField(required=True)
    class Meta:
        model = Post
        #sets hidden attributes that we don't want individual users filling out
        exclude = ['flag_count', 'verified','type']
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

    
    
