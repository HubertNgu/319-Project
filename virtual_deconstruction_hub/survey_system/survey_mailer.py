'''
 Survey Mailer module responsible for sending surveys to clients that have posted
 listings on the site.

 @author Hubert Ngu
'''

import logging
from util import constants
from listings.models import Listing
from mailer.views import send_survey_email
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def __is_survey_ready(listing):
    '''
    Returns true if a survey is ready to be mailed to a client.
    Note that the only surveys sent to this function as ones that
    have not expired.

    A survey is ready if:
        1) The survey has never been sent and
           the time now has passed the inital send delay
        2) The survey has been sent but we have passed
           the repeat send delay
    '''
    return (listing.survey_time_sent is None and 
            datetime.utcnow() > listing.created + \
                timedelta(days=constants.INITIAL_SEND_DELAY)) \
            or \
            (listing.survey_time_sent is not None and 
            datetime.utcnow() > listing.survey_time_sent + \
                timedelta(days=constants.REPEAT_SEND_DELAY))

def __expire_listings(listings):
    '''
    Expires listings that have passed their expiration date.
    '''
    for listing in listings:
        if datetime.utcnow() > listing.expires:
            listing.expired = True; listing.save()
            #logger.info('Listing %s has passed the expiry date and has been expired', listing)

def __send_survey(listing):
    '''
    Constructs the unique URL for the survey, updates the time sent
    and emails the survey.
    '''
    survey_url = '%s/survey/%s' % (constants.SITE, listing.uuid)    
    send_survey_email(survey_url, listing.creator)
    listing.survey_time_sent = datetime.utcnow()
    listing.save()
    logger.info('Sending survey to %s at %s', listing.creator, survey_url)

def __send_surveys(listings):
    '''
    Emails all surveys that are ready to be sent.
    '''
    counter = 0
    for listing in listings:
        if __is_survey_ready(listing):
            __send_survey(listing)
            counter += 1
    return counter
    logger.info('Finished sending all ready surveys')

def expire_and_mail_surveys():
    '''
    Expires and mails surveys. This is the only function that
    should be called in this module.
    '''
    listings = Listing.objects.filter(expired=False)
    __expire_listings(listings)
    return __send_surveys(listings)

