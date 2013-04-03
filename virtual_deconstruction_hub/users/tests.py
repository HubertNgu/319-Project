'''
 Unit tests for the survey_system app.

 @author Dennis Lau
'''
from util import constants
from datetime import datetime, timedelta
from listings.models import Listing
from users.views import signup,verifyemail
from users.models import UserProfile
from verificationapp.models import VerificationApp
from django.http import Http404, HttpRequest
from django.test import TestCase

class UserTest(TestCase):
    

    def test_signup(self):
     username = "testusersignup"
     email = "test@test.com"
     password  = "hihihihih"
     request = HttpRequest()
     request.method='POST'
     request.__setattr__('username',username)
     request.__setattr__('email',email)
     request.__setattr__('password',password)
     
     signup(request)
     try:
         user = Users(username = username)
         userprofile = UserProfile(username=username)
         verificationapp = VerificationApp(username= username)
         user.delete()
         userprofile.delete()
         verificationapp.delete()
         return True
     except:
        return False
 
    def test_verifyemail(self):
        username = "testverifyemail"
        email = "testtest@test.com"
        password = "123123"
        Userprofile = UserProfile(username = username)
        verificationapp = "1234567890"
        verapp = VerificationApp(username = username , verificationcode = verificationapp)
        verapp.save()
        request = HttpRequest()
        request.method = 'GET'
        request.QUERY_STRING = "username="+username+"&verificationcode=" + verificationapp
        verifyemail(request)
        try:
            verificationapp = VerificationApp(username = username)
            return False
        except:
            userprofilecheck = UserProfile(username = username)
            self.assertTrue(userprofilecheck.isverified, msg)
            userprofilecheck.delete()
            return True
    
            
        
        
         
     