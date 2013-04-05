"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from datetime import datetime, timedelta
import uuid

from listings.models import Listing

class ListingTest(TestCase):
        
    def create_listing(self):
        listing = Listing(creator = "test@example.com", address = "2205 lower mall", title = "test", text_content = "test description", for_sale = "sell")
        listing.save()
        return listing
        
    def test_mark_verified(self):
        listing = self.create_listing()
        self.assertFalse(listing.verified)
        listing.mark_verified()
        self.assertTrue(listing.verified)
    
    def test_is_verified(self):
        listing = self.create_listing()
        self.assertFalse(listing.verified)
        listing.mark_verified()
        self.assertTrue(listing.verified)

    def test_mark_modified(self):
        listing = self.create_listing()
        listing.mark_modified()
        self.assertTrue(listing.last_modified < datetime.now() +
            timedelta(minutes=1))
        
    def test_flag(self):
        listing = self.create_listing()
        self.assertEqual(listing.flag_count, 0)
        listing.flag()
        self.assertEqual(listing.flag_count, 1)
        listing.flag()
        self.assertEqual(listing.flag_count, 2)

    def test_is_expired(self):
        listing = self.create_listing()
        self.assertFalse(listing.is_expired())
        listing.expired = True
        self.assertTrue(listing.is_expired())
        
    def test_set_url(self):
        listing = self.create_listing()
        self.assertEqual(listing.url, '')
        listing.set_url('www.test.com')
        self.assertEqual(listing.url, 'www.test.com')
        listing.set_url('www.example.com')
        self.assertEqual(listing.url, 'www.example.com')
        
    def test_get_url(self):
        listing = self.create_listing()
        self.assertEqual(listing.url, '')
        listing.set_url('www.test.com')
        self.assertEqual(listing.url, 'www.test.com')
        listing.set_url('www.example.com')
        self.assertEqual(listing.url, 'www.example.com')
    
    def test_get_creator(self):
        listing = self.create_listing()
        self.assertEqual(listing.creator, "test@example.com")
        listing.creator = "example@test.com"
        self.assertNotEqual(listing.creator, "test@example.com")
        self.assertEqual(listing.creator, "example@test.com")
    
    def test_get_last_modified_time(self):
        listing = self.create_listing()
        listing.mark_modified()
        self.assertTrue(listing.last_modified < datetime.now() + 
            timedelta(minutes=1))

    def test_get_title(self):
        listing = self.create_listing()
        self.assertEqual(listing.title,"test")
        listing.title = "test2"
        self.assertEqual(listing.title, "test2")
    
    def test_set_title(self):
        listing = self.create_listing()
        self.assertEqual(listing.title, "test")
        listing.set_title("test1")
        self.assertEqual(listing.title, "test1")
        listing.set_title("test2")
        self.assertEqual(listing.title , "test2")

    def test_get_text_content(self):
        listing = self.create_listing()
        self.assertEqual(listing.text_content, "test description")
        listing.text_content = "edited"
        self.assertEqual(listing.text_content, "edited")
    
    def test_set_text_content(self):
        listing = self.create_listing()
        self.assertEqual(listing.text_content, "test description")
        listing.set_text_content("edited")
        self.assertEqual(listing.text_content, "edited")
        
    def test_increment_flags(self):
        listing = self.create_listing()
        self.assertEqual(listing.flag_count, 0)
        listing.increment_flags()
        self.assertEqual(listing.flag_count, 1)
        listing.increment_flags()
        self.assertEqual(listing.flag_count, 2)
        
    def test_get_flag_count(self):
        listing = self.create_listing()
        self.assertEqual(listing.flag_count, 0)
        listing.increment_flags()
        self.assertEqual(listing.flag_count, 1)
        listing.increment_flags()
        self.assertEqual(listing.flag_count, 2)
    
    def test_get_uuid(self):
        listing = self.create_listing()
        self.assertIsNotNone(listing.uuid)
        new_uuid = uuid.uuid4()
        listing.uuid = new_uuid
        self.assertIsNotNone(listing.uuid)
        self.assertEqual(listing.uuid, new_uuid)
    
    def test_get_city(self):
        listing = self.create_listing()
        self.assertIsNotNone(listing.city)
        self.assertEqual(listing.city, 'Vancouver')
        listing.city = 'Burnaby'
        self.assertEqual(listing.city, 'Burnaby')