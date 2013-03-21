from django.http import Http404
#from posts.views import search_posts
from listings.models import Listing
from posts.models import Post
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet 
from haystack.views import SearchView, search_view_factory
#from posts.search_indexes import SearchForm, PostSearchView
from haystack.forms import HighlightedSearchForm
from haystack.inputs import AutoQuery, Exact
from listings.models import get_listings_categories, get_sale_categories
from django import forms
import logging

logger = logging.getLogger(__name__)

TEMPLATE_PATHS = {'posts_results': 'search/posts_search.html',
                  'listings_results': 'search/listings_search.html'}

"""Directs the query string from user to appropriate search method by the appropriate type based on the select drop down value selected from global search bar"""
def search(request):
    # only process if HTTP request method is GET
    # raise 404 error if POST header
    if request.method == 'GET':
        search_type = request.GET.get('type', None)
        # call relevant method based on type query string
        if search_type == "list":
            # if its a list type direct to listings search
            return search_listings_custom_form(request)
        elif search_type == "blog" or search_type == "proj" or search_type == "stry":
            # if valid post type direct to posts search
            return search_posts_custom_form(request)
        else: raise Http404
    else: raise Http404

            
#
#"""Searches the query string and post type selected from dropdown menu in global search bar"""
#def search_posts(request):
#    post_type = request.GET.get('type', None)
#    if post_type:
#        post_type = str(post_type).lower() 
#    q_string = request.GET['q']
#    sqs = SearchQuerySet().filter(content=AutoQuery(q_string), type=Exact(post_type))
#    view = search_view_factory(
#        view_class=SearchView,
#        template=TEMPLATE_PATHS['posts_results'],
#        searchqueryset=sqs,
#        form_class=HighlightedSearchForm, 
#        )
#    return view(request)

"""Searches the query string and post type selected from dropdown menu in global search bar"""
def search_posts_custom_form(request):
    post_type = request.GET.get('type', None)
    if post_type:
        post_type = str(post_type).lower() 
    q_string = request.GET['q']
    sqs = SearchQuerySet().filter(content=AutoQuery(q_string), type=Exact(post_type))
    #sqs = SearchQuerySet().filter(content=AutoQuery(q_string)).models(Post).facet('type')
    view = search_view_factory(
        view_class=PostSearchView,
        template=TEMPLATE_PATHS['posts_results'],
        searchqueryset=sqs,
        form_class=PostSearchForm, 
        )
    return view(request)

#"""Searches the query string for in listings objects"""
#def search_listings(request):
#    q_string = request.GET['q']
#    #category = request.GET.get('category', None)
#    sqs = SearchQuerySet().filter(content=AutoQuery(q_string)).models(Listing)
##    if category:
##        category = str(category).lower() 
##        sqs = SearchQuerySet().filter(content=AutoQuery(q_string), category=Exact(category)).models(Listing)
#    view = search_view_factory(
#        view_class=SearchView,
#        template=TEMPLATE_PATHS['listings_results'],
#        searchqueryset=sqs,
#        form_class=HighlightedSearchForm
#        )
#    return view(request)

"""Searches the query string for in listings objects"""
def search_listings_custom_form(request):
    q_string = request.GET['q']
    #category = request.GET.get('category', None)
    sqs = SearchQuerySet().filter(content=AutoQuery(q_string)).models(Listing).facet('category').facet('for_sale')
#    if category:
#        category = str(category).lower() 
#        sqs = SearchQuerySet().filter(content=AutoQuery(q_string), category=Exact(category)).models(Listing)
    view = search_view_factory(
        view_class=ListingSearchView,
        template=TEMPLATE_PATHS['listings_results'],
        searchqueryset=sqs,
        form_class=ListingSearchForm
        )
    return view(request)


class ListingSearchForm(SearchForm):
    cat = forms.CharField(required=False, widget=forms.Select(choices=get_listings_categories()))
    type = forms.CharField(required=False, widget=forms.HiddenInput)
    TYPE_CHOICES=((True, 'Items for sale'),
                  (False, 'Items wanted'))
    for_sale = forms.BooleanField(required=False, widget=forms.Select(choices=get_sale_categories()))
    
    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(ListingSearchForm, self).search()
           
        # Check to see if a category_date was chosen.
        if self.cleaned_data.get('cat', None):
            sqs = sqs.filter(category=self.cleaned_data['cat'])
            
        if self.cleaned_data.get('for_sale', None):
            sqs = sqs.filter(for_sale__contains=self.cleaned_data.get('for_sale'))

        return sqs
    
    
class ListingSearchView(SearchView):
    
    def extra_context(self):
            extra = super(ListingSearchView, self).extra_context()

            extra['post_type'] = self.request.GET.get('type', None)
            extra['cat'] = self.request.GET.get('cat', None)
            extra['for_sale'] = self.request.GET.get('for_sale', None)

            return extra
    
class PostSearchForm(SearchForm):
    type = forms.CharField(required=False, widget=forms.HiddenInput)
    
    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(PostSearchForm, self).search()
           
        # Check to see if a type was chosen.
        if self.cleaned_data.get('type', None):
            sqs = sqs.filter(type=self.cleaned_data['type'])

        return sqs
    
class PostSearchView(SearchView):
    
    def extra_context(self):
            extra = super(PostSearchView, self).extra_context()

            extra['post_type'] = self.request.GET.get('type')

            return extra
    
