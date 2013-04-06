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
from django.contrib.auth import authenticate,login,get_user

class UserTest(TestCase):
   

   
    def test_signup(self):
        username = "testusersignup"
        firstname = "graham"
        lastname = "haroldson"
        email = "test@test.com"
        password  = "hihihihih"
        phone = "999999999";
        address = "address";
        province = "BC";
        city = "city";
        request = HttpRequest()
        request.method='POST'
        request.__setattr__('username',username)
        request.__setattr__('firstname',firstname)
        request.__setattr__('lastname',lastname)
        request.__setattr__('email',email)
        request.__setattr__('password',password)
        request.__setattr__('phone', phone);
        request.__setattr__('address', address);
        request.__setattr__('province', province);
        request.__setattr__('city', city);
        signup(request)
        try:
            user = Users(username = username)
            userprofile = UserProfile(username=username)
            verificationapp = VerificationApp(username= username )
            self.assertTrue(userprofile.firstname == firstname)
            self.assertTrue(userprofile.lastname == lastname)
            self.assertTrue(userprofile.email == email)
            self.assertTrue(userprofile.phone == phone)
            self.assertTrue(userprofile.address == address)
            self.assertTrue(userprofile.province == province)
            self.assertTrue(userprofile.city == city)
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
    
    def test_editAccount(self):
        username = "testusersignup"
        firstname = "graham"
        lastname = "haroldson"
        email = "test@test.com"
        password  = "hihihihih"
        phone = "999999999";
        address = "address";
        province = "BC";
        city = "city";
        
        password = "hi"
        firstname2 = "sean"
        lastname2 = "slipetz"
        email2 = "new@test.com"
        phone2 = "11111111";
        address2 = "newaddress";
        province2 = "BC";
        city2 = "newcity";
        
        request = HttpRequest()
        request.method='POST'
        request.__setattr__('username',username)
        request.__setattr__('firstname',firstname)
        request.__setattr__('lastname',lastname)
        request.__setattr__('email',email)
        request.__setattr__('password',password)
        request.__setattr__('phone', phone);
        request.__setattr__('address', address);
        request.__setattr__('province', province);
        request.__setattr__('city', city);
        signup(request)
        try:
            user = Users(username = username)
            userprofile = UserProfile(username=username)

            self.assertTrue(user.password == password)
            self.assertTrue(user.firstname == firstname)
            self.assertTrue(user.lastname == lastname)
            self.assertTrue(user.email == email)
            self.assertTrue(user.phone == phone)
            self.assertTrue(user.address == address)
            self.assertTrue(user.province == province)
            self.assertTrue(user.city == city)   
            
            request.__setattr__('firstname',firstname2)
            request.__setattr__('lastname',lastname2)
            request.__setattr__('email',email2)
            request.__setattr__('phone', phone2);
            request.__setattr__('address', address2);
            request.__setattr__('province', province2);
            request.__setattr__('city', city2);
            request.__setattr__('password', password2);
            editaccount(request)
            
            user = Users(username = username)
            userprofile = UserProfile(username=username)
            
            self.assertTrue(user.password == password2)
            self.assertTrue(user.firstname == firstname2)
            self.assertTrue(user.lastname == lastname2)
            self.assertTrue(user.email == email2)
            self.assertTrue(user.phone == phone2)
            self.assertTrue(user.address == address2)
            self.assertTrue(user.province == province2)
            self.assertTrue(user.city == city2)   
            
            user.delete()
            userprofile.delete()
            verificationapp.delete()
            return True
        except:
            return False
        
        
         
     