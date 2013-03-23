'''
 Views module for the statistics generator.

 @author Hubert Ngu
 @author Jason Hou
'''

import logging
from django.shortcuts import render
from survey_system.models import Survey
from statistics_generator.models import Statistics, StatisticsCategory

logger = logging.getLogger(__name__)

def index(request):
    '''
    Loads the index page showing all of the statistics from the last generated
    run of the statistics_generator.
    '''

    # Handle user account options.
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]


    # If there have never been any statistics generated then return the
    # none page for statistics
    try:
        statistics = Statistics.objects.latest('id')
        logger.debug('Successfully found the lastest Statistics instance')
    except:
        return render(request, 'statistics_generator/statistics_none.html')
    
    statistics_categories = StatisticsCategory.objects.filter(statistics_id=statistics.id)
    categories, survey_count, buyer_count, seller_count, category_amount = \
        list(), list(), list(), list(), list()

    # Create parallel lists for the graphs
    for statistic_category in statistics_categories:
        categories.append(str(statistic_category.category))
        survey_count.append(int(statistic_category.survey_count))
        buyer_count.append(int(statistic_category.buyer_count))
        seller_count.append(int(statistic_category.seller_count))
        category_amount.append(int(statistic_category.amount))                        
    # Transform the lists to formatted strings using the values
    labels = str(categories)[1:-1].replace(', ', '|').replace('\'', '').replace(' ', '+')
    category_survey_values = 't:%s' % str(survey_count)[1:-1]
    category_buyer_values = 't:%s' % str(buyer_count)[1:-1]
    category_seller_values = 't:%s' % str(seller_count)[1:-1]
    category_amount_values = 't:%s' % str(category_amount)[1:-1]
    logger.debug('Successfully formatted statistics labels and values for graphs')

    # Build values dictionary that will be used by the html page to load values.
    values = dict()
    values['category_amount_max'] = max(category_amount)
    values['number_surveys'] = int(statistics.number_surveys)
    values['number_listings'] = int(statistics.number_listings)
    values['number_buyer_surveys'] = int(statistics.number_buyer_surveys)
    values['number_seller_surveys'] = int(statistics.number_seller_surveys)
    values['number_buyer_listings'] = int(statistics.number_buyer_listings)
    values['number_seller_listings'] = int(statistics.number_seller_listings)
    values['average_transaction_amount'] = statistics.average_transaction_amount
    values['buyer_transaction_amount'] = statistics.buyer_transaction_amount
    values['seller_transaction_amount'] = statistics.seller_transaction_amount
    values['successful_transaction_amount'] = statistics.successful_transaction_amount
    values['average_transaction_time'] = statistics.average_transaction_time
    values['buyer_transaction_success_rate'] = statistics.buyer_transaction_success_rate
    values['seller_transaction_success_rate'] = statistics.seller_transaction_success_rate
    values['total_transaction_success_rate'] = statistics.total_transaction_success_rate
    values['labels'] = labels
    values['category_survey_values'] = category_survey_values
    values['category_buyer_values'] = category_buyer_values
    values['category_seller_values'] = category_seller_values
    values['category_amount_values'] = category_amount_values
    
    return render(request, 'statistics_generator/statistics_main.html', values)
