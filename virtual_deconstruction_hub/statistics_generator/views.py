import re
import logging
from listings.views import Listing
from survey_system.models import Survey
from listings.models import Listing, ListingForm
from statistics_generator.models import Statistics, StatisticsCategory
from gmapi import maps
from gmapi.forms.widgets import GoogleMap
from django import forms
from django.utils import timezone
from django.http import HttpResponse, HttpRequest
from django.template.defaulttags import csrf_token
from django.template import Context, loader, RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect,get_object_or_404, render_to_response, render

logger = logging.getLogger(__name__)

class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))

def index(request):
	# If there have never been any statistics generated then return the
	# none page for statistics
	try:
		statistics = Statistics.objects.latest('id')
	except:
		return render(request, 'statistics_generator/statistics_none.html')
	successful_transaction_amount = statistics.successful_transaction_amount
	average_transaction_time = statistics.average_transaction_time
	transaction_success_rate = statistics.transaction_success_rate
	
	statistics_categories = StatisticsCategory.objects.filter(statistics_id=statistics.id)
	categories, survey_count, buyer_count, seller_count, amount = \
		list(), list(), list(), list(), list()

	# Create parallel lists
	for statistic_category in statistics_categories:
		categories.append(str(statistic_category.category))
		survey_count.append(int(statistic_category.survey_count))
		buyer_count.append(int(statistic_category.buyer_count))
		seller_count.append(int(statistic_category.seller_count))
		amount.append(int(statistic_category.amount))

	logger.debug("debug me baby")

							
	labels = str(categories)[1:-1].replace(', ', '|').replace('\'', '')
	category_survey_values = 't:%s' % str(survey_count)[1:-1]
	logger.debug('%s', category_survey_values)


	category_buyer_values = 't:%s' % str(buyer_count)[1:-1]
	category_seller_values = 't:%s' % str(seller_count)[1:-1]
	category_amount_values = 't:%s' % str(amount)[1:-1]

	logger.debug('%s', category_amount_values)

	values = dict()
	values['successful_transaction_amount'] = successful_transaction_amount
	values['average_transaction_time'] = average_transaction_time
	values['transaction_success_rate'] = transaction_success_rate
	values['labels'] = labels
	values['category_survey_values'] = category_survey_values
	values['category_buyer_values'] = category_buyer_values
	values['category_seller_values'] = category_seller_values
	values['category_amount_values'] = category_amount_values

	gmap = maps.Map(opts = {
        'center': maps.LatLng(38, -97),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 3,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    
	values['form'] =  MapForm(initial={'map': gmap})
    
	return render(request, 'statistics_generator/statistics_main.html', values)
