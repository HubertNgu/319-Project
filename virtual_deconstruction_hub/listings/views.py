# Create your views here.

from django.http import HttpResponse

def index(request):
    return HttpResponse("Buying && Selling")

def detail(request, listing_id):
    return HttpResponse("Listing title: %s" % listing_title)


