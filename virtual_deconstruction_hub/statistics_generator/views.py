from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect,get_object_or_404, render_to_response, render
from django.template import Context, loader, RequestContext
from django.template.defaulttags import csrf_token
from django import forms
from survey_system.models import Survey
from listings.models import Listing, ListingForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
import re
from listings.views import Listing
from statistics_generator.models import Statistics, StatisticsCategory

def index(request):
	# If there have never been any statistics generated then return the
	# none page for statistics
	try:
		statistics = Statistics.objects.latest('id')
	except:
		return render(request, 'statistics_generator/statistics_none.html')

	statistics_categories = StatisticsCategory.objects.get(statistics_id=statistics.id)
	successful_transaction_amount = statistics.successful_transaction_amount
	average_transaction_time = statistics.average_transaction_time
	transaction_success_rate = statistics.transaction_success_rate

	categories, survey_count, buyer_counter, seller_count, amount = \
		list(), list(), list(), list(), 0

	# Create parallel lists
	for statistic_category in statistics_categories:
		cateogies.append(statistic_category.category)
		survey_count.append(statistic_category.survey_count)
		
							
	labels = str(cateogies)[1:-1].replace(', ', '|')

		
	return render(request, 'statistics_generator/statistics_main.html', 
		{'successful_transaction_amount' : successful_transaction_amount, 
		'labels' : labels})
