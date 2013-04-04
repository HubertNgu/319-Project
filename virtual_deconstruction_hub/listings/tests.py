"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from datetime import datetime, timedelta
import uuid

class SimpleTest(TestCase):

        
    def create_listing(self):
        listing = Listing(creator = "test@example.com", address = "2205 lower mall", title = "test", text_content = "test description", for_sale = "sell")
        listing.save()
        return listing
        
    def test_mark_verified(self):
        listing = self.create_listing
        self.assertFalse(listing.verified)
        listing.mark_verified
        listing.save
        self.assertTrue(listing.verified)
    
    def test_is_verified(self):
        listing = self.create_listing
        self.assertFalse(listing.is_verified)
        listing.mark_verified()
        self.assertTrue(listing.is_verified)

    def test_mark_modified(self):
        listing = self.create_listing()
        listing.mark_modified
        self.assertTrue(listing.modified < timezone.now() + datetime.timedelta(minutes=1))
        
    def test_flag(self):
        listing = self.create_listing()
        self.assertEqual(listing.flag_count, 0)
        listing.flag
        self.assertEqual(listing.flag_count, 1)
        listing.flag
        self.assertEqual(listing.flag_count, 2)

    def test_is_expired(self):
        listing = self.create_listing()
        self.assertFalse(listing.is_expired)
        listing.expired = True
        self.assertTrue(listing.is_expired)
        
    def test_set_url(self):
        listing = self.create_listing()
        self.assertTrue(listing.url is None)
        listing.set_url(listing, 'www.test.com')
        listing.save
        self.assertEqual(listing.url, 'www.test.com')
        listing.set_url(listing, 'www.example.com')
        listing.save
        self.assertEqual(listing.url, 'www.example.com')
        
    def test_get_url(self):
        listing = self.create_listing()
        self.assertEqual(listing.url is None)
        listing.set_url(listing, 'www.test.com')
        listing.save
        self.assertEqual(listing.get_url, 'www.test.com')
        listing.set_url(listing, 'www.example.com')
        listing.save
        self.assertEqual(listing.get_url, 'www.example.com')
    
    def test_get_creator(self):
        listing = self.create_listing()
        self.assertEqual(listing.creator, "test@example.com")
        listing.creator = "example@test.com"
        listing.save
        self.assertFalse(listing.creator is "test@example.com")
        self.assertTrue(listing.creator is "example@test.com")
    
    
    def test_get_created_time(self):
        listing = self.create_listing()        
        return self.created

    def test_get_last_modified_time(self):
        listing = self.create_listing()
        listing.mark_modified
        listing.save
        self.assertTrue(listing.get_last_modified_time
                        < timezone.now() + datetime.timedelta(minutes=1))

    def test_get_title(self):
        listing = self.create_listing()
        self.assertEqual(listing.get_title,"test")
        listing.title = "test2"
        self.assertEqual(listing.get_title, "test2")
    
    def test_set_title(self):
        listing = self.create_listing()
        self.assertEqual(listing.title, "test")
        listing.set_title(listing, "test1")
        self.assertEqual(listing.title, "test1")
        listing.set_title(listing, "test2")
        self.assertEqual(listing.title , "test2")

    def test_get_text_content(self):
        listing = self.create_listing()
        self.assertEqual(listing.get_text_content, "test description")
        listing.text_content = "edited"
        self.assertEqual(listing.get_text_content, "edited")
    
    def test_set_text_content(self):
        listing = self.create_listing()
        self.assertEqual(listing.text_content, "test description")
        listing.set_text_content(listing, "edited")
        self.assertEqual(listing.text_content, "edited")
        
    def test_increment_flags(self):
        listing = self.create_listing()
        self.assertEqual(listing.flag_count, 0)
        listing.increment_flags(listing)
        self.assertEqual(listing.flag_count, 1)
        listing.increment_flags(listing)
        self.assertEqual(listing.flag_count, 2)
        
    def test_get_flag_count(self):
        listing = self.create_listing()
        self.assertEqual(listing.get_flag_count, 0)
        listing.increment_flags(listing)
        self.assertEqual(listing.get_flag_count, 1)
        listing.increment_flags(listing)
        self.assertEqual(listing.get_flag_count, 2)
    
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
    
    def test_get_listings_categories():
        listing = self.create_listing()
        categories = ['Woods', 'Bricks', 'Shingles', 'Drywall', 'Toilets', 'Sinks',
                'Tubs', 'Windows', 'Doors', 'Fixtures', 'Cable and Wiring', 
                'Particle board', 'Cardboard', 'Cabinetry', 'Scrap metal',
                'Appliances', 'Other']
        cat_choices = [(category, category) for category in categories]
        assertEqual(listing.get_listings_categories(), cat_choices)
        
    def test_get_sale_categories():
        listing = self.create_listing()
        sale_choices=[("sell", 'Items for sale'), ("want", 'Items wanted')]
        assertEqual(listing.get_sale_categories(), sale_choices)

    def test_get_city_categories():
        listing = self.create_listing()
        cities = ['Abbotsford', 'Burnaby', 'Chilliwack',
             'Coquitlam', 'Delta', 'Hope', 'Langley', 'Maple Ridge',
             'Mission', 'New Westminster', 'North Vancouver', 'Pitt Meadows',
             'Port Coquitlam', 'Port Moody', 'Richmond', 'Squamish', 'Surrey',
             'Vancouver', 'West Vancouver', 'White Rock', 'Whistler']
        city_choices = [(city, city) for city in cities]
        assertEqual(listing.get_city_categories(), city_choices)
        
        
