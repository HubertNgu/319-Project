from django.db import models
from django import forms
from django.forms import ModelForm
import uuid
import os
from django.conf import settings

TIME_ZONE = settings.TIME_ZONE

# Create your models here.
class Post(models.Model):
    """The model for a Post objects in the database.
    
    The following fields are required for object creation:
    
    url = an relative, unique url tag in http acceptable format that is a maximum of 110 characters
    creator = the email of the person creating the post
    title = the title of the post, maximum of 100 characters
    text_content = The text content of the post, max is determined by the specific database in use 
    type = must be one of "blog", "user" or "proj" for Blog, User Story or Project Idea 
    
    The following fields are are automatically set at object creation/modifcation:
    
    created = the date and time the post was created
    last_modified = the date and time of the last post modification
    verified = whether or not the post has been verified, defaults to False
    flag_count = the number of times the post has been flagged as innapropriate by users, defaults to 0
    uuid = a 36 character universally unique identifier, generated automatically at post creation
    
    """
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
        """ Marks a post object as verified,
        sets post.verified = True
        """
        self.verified = True
        
    def is_verified(self):
        """ Returns True if a post is verified,
        else returns False.
        """
        return self.verified
    
    def __unicode__(self):
        """ Returns a unicode string representation of 
        the post object, in this case it returns
        the posts title.
        """
        return self.title
    
    def renew(self):
        """ Calls the save method on an object so
        that it's last_modified time is updated.
        """
        self.save()

    def get_type(self):
        """ Returns the string value from the post objects
        type field which is one of: "blog", "stry" or "proj"
        """
        return self.type
     
    def set_type(self, t):
        """ Sets the value of the post objects
        type field,
        
        Arguments:
        t -- a 4 character string, must be one of: "blog", "stry" or "proj"
        """
        self.type = t
        
    def set_url(self, u):
        """ Sets the value of the post objects
        url tag field. 
        
        Arguments:
        u -- an http acceptable unique (to the posts table) string, maximum length 110 characters.
        """
        self.url = u
        
    def get_url(self):
        """ Returns the string value of the post objects
        url tag field.
        """
        return self.url
    
    def get_creator(self):
        """ Returns the string value of the post objects
        creator field, this will be an email address.
        """
        return self.creator
    
    def get_created_time(self):
        """ Returns the the date and time the post object
        was created in DateTime format. 
        """
        return self.created

    def get_last_modified_time(self):
        """ Returns the the date and time the post object
        was last modified in DateTime format. 
        """
        return self.last_modified

    def get_title(self):
        """ Returns the string value of the post objects
        title field.
        """
        return self.title
    
    def set_title(self, t):
        """ Sets the string value of the post objects
        title field to t.
    
        Arguments:
        t -- a string, maximum length 100 characters.
        """
        self.title = t

    def get_text_content(self):
        """ Returns the value of the post objects
        text_content field.
        """
        return self.text_content
    
    def set_text_content(self, t):
        """ Sets the value of the post objects
        text_content field to t.
        
        Arguments:
        t -- a string, maximum length determined by the
        database backends implementation of TextField.
        Usually this is quite large (ie thousands of 
        characters).
        """
        self.text_content = t
    
    def increment_flags(self):
        """ Increment the current integer value of the post
        objects flag field by one.
        """
        self.flag_count += 1
    
    def get_flag_count(self):
        """ Returns the current integer value of the post
        objects flag field.
        """
        return self.flag_count
    
    def get_uuid(self):
        """ Returns the 36 character string value of
        the post objects uuid field.
        """
        return self.uuid
    
# Create the form class.
class PostForm(ModelForm):
    """ A model for the form representation of a post object.
    This is used for displaying to the user only the fields
    desired for them to fill out in order to create a post.
    The PostForm class also adds an email verification field
    that is mandatory for a user to fill out and must match 
    the primary email field before a form is validated. This
    is done to ensure that a user that does not have an account
    does not accidentally enter an incorrect email address as
    they would not be able to verify or edit their post without
    the unique link emailed to them by the system upon post
    creation. Users that have registered an account and are
    logged in will not see these fields. 
    """
    creator = forms.EmailField(required=True)
    email_verification = forms.EmailField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs) 
        self.fields['creator'].label = "Email address"
        self.fields['email_verification'].label = "Verify email"

    class Meta:
        """ Models the form based on the Post model directly, one form
        field for each Post model field.
        """
        model = Post
        #sets which fields displayed when form is rendered and their order.
        fields = ['creator', 'email_verification', 'title', 'text_content']
        
    def clean(self):
        """ Overrides the default Form clean method (for form validation)
        to utilize the creator and email_verification fields and set an
        appropriate error message to be rendered should they not match. 
        """
        cleaned_data = self.cleaned_data
        creator_email = cleaned_data.get("creator")
        verified_email = cleaned_data.get("email_verification")

        if creator_email != verified_email:
            self._errors["email_verification"] = self.error_class(["The email and verification entered do not match."])

        # Always return the full collection of cleaned data.
        return cleaned_data
    
    def get_type(self):
        return "PostForm"
        
class EditPostForm(ModelForm):
    """ A model for the form representation of a post object.
    This is used for displaying to the user only the fields
    desired for them to fill out in order to edit an existing post.
    """
    class Meta:
        """ Models the form based on the Post model directly, one form
        field for each Post model field.
        """
        model = Post
        #sets which fields displayed when form is rendered and their order.
        fields = ['title', 'text_content']
        
    def get_type(self):
        return "EditPostForm"
        
    
class Photo(models.Model):
    """The model for a Photo object in the database. 
    Each photo is a child to exactly one Post object. 
    There can be many photos childed to a single post. 
    
    The following fields are required for object creation:
    
    post = the post object to which the photo is childed
    photo =  the image file being uploaded to the server
    
    The following fields are optional:
    
    caption = a string describing the photo, maximum 200 characters
    """
    post = models.ForeignKey(Post)
    photo =  models.ImageField(upload_to='photos/posts/%Y/%B/%d/')
    caption = models.CharField(max_length=200)
    
    def get_caption(self):
        """ Returns the string value of the
        caption field for the photo object.
        """
        return self.caption
    
    def get_url(self):
        """ Returns the string value of the 
        photo field for the photo object.
        This is the file name of
        the photo after it has been uploaded
        and can be used as a relative url to
        view the image.
        """
        return self.photo
    
    def imagename(self):
        """ Returns the string value of the 
        absolute path for the photo object.
        This is the path and file name of
        the photo after it has been uploaded
        and can be used as an absolute url to
        view the image.
        """
        return os.path.basename(self.photo.name)

   
class UploadForm(forms.Form):
    """ A model for the form representation of a photo object
    to display to users for the purpose of uploading a photo 
    to be attached to a specific post object. A post object
    can have many photos attached to it but a photo may only 
    be attached to a single post.
    """
    picture  = forms.ImageField(label='Add a picture')
    caption = forms.CharField(label = 'Add a caption for your picture',required=False)
