from django.http import Http404
from listings.models import Listing
from haystack.forms import SearchForm, FacetedSearchForm
from haystack.query import SearchQuerySet 
from haystack.views import SearchView, search_view_factory
from haystack.inputs import AutoQuery, Exact
from listings.models import get_listings_categories, get_sale_categories, get_city_categories
from django import forms
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Dictionary of pairings for relative template paths. Every rendering of a template for a search references it's specific key and uses the associated
# template path from this dictionary. For example, a listings search will use the callue associated with the 'listings_results' key if asked 
# render the results of a search for listings objects. This dictionary provides a single point for making template changes without having to 
# edit any other section of code in this file.  
TEMPLATE_PATHS = {'posts_results': 'search/posts_search.html',
                  'listings_results': 'search/listings_search.html'}


def search(request):
    """Directs the query string from user to appropriate search method for the
    specified type based on the select drop down value selected from the global
    search bar
    
    Arguments:
    
    request -- the HTTP request from the users browser    
    """
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



def search_posts_custom_form(request):
    """Searches only post objects using the query string and specific 
    post type selected from the dropdown menu in the global search bar
    
    Arguments:
    
    request -- the HTTP request from the users browser 
    """
    post_type = request.GET.get('type', None)
    if post_type:
        post_type = str(post_type).lower() 
    q_string = request.GET['q']
    sqs = SearchQuerySet().filter(content=AutoQuery(q_string), type=Exact(post_type))
    view = search_view_factory(
        view_class=PostSearchView,
        template=TEMPLATE_PATHS['posts_results'],
        searchqueryset=sqs,
        form_class=PostSearchForm, 
        )
    return view(request)


"""Searches the query string for in listings objects"""
def search_listings_custom_form(request):
    """Searches only listings objects using the query string and any
    filters selected from the search filter page.
    
    Arguments:
    
    request -- the HTTP request from the users browser 
    """
    view = search_view_factory(
        view_class=ListingSearchView,
        template=TEMPLATE_PATHS['listings_results'],
        searchqueryset=SearchQuerySet().models(Listing),
        form_class=ListingSearchForm
        )
    return view(request)


class ListingSearchForm(SearchForm):
    """ A model for the form representation of a the searchable
    fields for listings objects. This is used for displaying 
    to the user only the fields that they are able to filter
    search results by and allows users to filter based on the
    category, sale type and city fields of a listing object.
    (The type field referenced in this form is not used in
    searching, however it is necessary to differentiate a 
    listing objects search from a posts objects search)  
    """
    category = forms.CharField(required=False, widget=forms.Select(choices=get_listings_categories()))
    type = forms.CharField(required=False, widget=forms.HiddenInput)
    for_sale = forms.CharField(required=False, widget=forms.Select(choices=get_sale_categories()))
    city = forms.CharField(required=False, widget=forms.Select(choices=get_city_categories()))
    q = forms.CharField(required=False, label=('Search'), widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(ListingSearchForm, self).__init__(*args, **kwargs)
        self.fields['city'].label = "City"
        self.fields['for_sale'].label = "Type of listing"
        self.fields['cat'].label = "Category"
    
    
    def search(self):
        """ The method that is run when a user clicks filter 
        on the listings search results page. This method builds
        the query based on the options selected by the user then
        executes returns a paginated list of the results.  
        """
        # First, store the SearchQuerySet received from other processing.
        sqs = super(ListingSearchForm, self).search()
            
        # Check to see if a category was chosen.
        if self.cleaned_data['category']:
            sqs = sqs.filter(category=self.cleaned_data['category'])
            
        # Check to see if a type was chosen.
        if self.cleaned_data['for_sale']:
            sqs = sqs.filter(for_sale=self.cleaned_data['for_sale'])
            
        # Check to see if a city was chosen.
        if self.cleaned_data['city']:
            sqs = sqs.filter(city=self.cleaned_data['city'])

        return sqs.order_by('-last_modified')
    
    
class ListingSearchView(SearchView):
    """ An extension of the default search results view.
    The default view only works with one query parameter 'q',
    so this view is necessary in order to allow searching and
    displaying results based on the additional parameters in the
    ListingSearchForm model.
    """    
    def __init__(self, *args, **kwargs):
        super(ListingSearchView, self).__init__(*args, **kwargs)
        results_per_page = int(settings.LISTINGS_PAGE_SIZE) 
        if not results_per_page is None:
            self.results_per_page = results_per_page
    
    def extra_context(self):
        """ Defines the extra content used in the search view
        """
        extra = super(ListingSearchView, self).extra_context()

        extra['post_type'] = self.request.GET.get('type', None)
        extra['category'] = self.request.GET.get('category', None)
        extra['for_sale'] = self.request.GET.get('for_sale', None)
        extra['city'] = self.request.GET.get('city', None)

        return extra
    
class PostSearchForm(SearchForm):
    """ A model for the form representation of a the searchable
    fields for post objects. This is used for displaying 
    to the user only the fields that they are able to filter
    search results by and allows users to filter based only on 
    the type of a post object (blog, proj or stry).
    """
    type = forms.CharField(required=False, widget=forms.HiddenInput)
    
    def search(self):
        """ The method that is run when a user clicks search 
        on the global search bar with on of the three post types
        selected. This method builds the query from the search
        string entered by the user then executes returns a 
        paginated list of the results.  
        """
        # First, store the SearchQuerySet received from other processing.
        sqs = super(PostSearchForm, self).search()
           
        # Check to see if a type was chosen.
        if self.cleaned_data.get('type', None):
            sqs = sqs.filter(type=self.cleaned_data['type'])

        return sqs.order_by('-created')
    
class PostSearchView(SearchView):
    """ An extension of the default search results view.
    The default view only works with one query parameter 'q',
    so this view is necessary in order to allow searching and
    displaying results based on the additional parameters in the
    PostSearchForm model.
    """
    def __init__(self, *args, **kwargs):
        super(PostSearchView, self).__init__(*args, **kwargs)
        results_per_page = int(settings.POSTS_PAGE_SIZE) 
        if not results_per_page is None:
            self.results_per_page = results_per_page
    
    def extra_context(self):
        """ Defines the extra content used in the search view
        """
        extra = super(PostSearchView, self).extra_context()

        extra['post_type'] = self.request.GET.get('type')

        return extra

