from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context, loader
from listings.models import Listing
from django.shortcuts import render_to_response


def index(request):
    listings_list = Listing.objects.order_by('created')
    context = {'listings_list': listings_list}

    return render(request, 'listings/listings_list.html', context)

def detail(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    context = {'listing':listing}
    return render(request, 'listings/listings_individual.html', context)

def searchListing(request):
    if request.method == 'SEARCH':
        keyword = request.SEARCH.get('keyword')
        listings_results = Listing.objects.raw('SELECT * FROM listings WHERE title LIKE %%s%', [keyword])
        context=Context({
                     'listings_list' : listings_results,
                     })
        return HttpResponse(HttpResponse(template.render(context)))

def filterListing(request, listing_type):
    if(listing_type == 'Items for sale'):
        listings_results = Listing.objects.raw('SELECT * FROM listings WHERE type == "Items for sale" ')
        context=Context({
                     'listings_list' : listings_results,
                     })
        return HttpResponse(HttpResponse(template.render(context)))
    if(listings_type == 'Wanted items'):
        listings_results = Listing.objects.raw('SELECT * FROM listings WHERE type == "Wanted Items" ')
        context=Context({
                     'listings_list' : listings_results,
                     })
        return HttpResponse(HttpResponse(template.render(context)))
        
def createListing(request):
    if request.method == 'POST':
        creator = request.POST.get('creator')
        title = request.POST.get('title')
        textContext = request.POST.get('textContext')
        photo1 = request.POST.get('photo1')
        photo2 = request.POST.get('photo2')
        photo3 = request.POST.get('photo2')
        photo4 = request.POST.get('photo2')
        new_listing = Listing.object.create_listing(cls, creator, title, textContext, 
                                                    photo1, photo2, photo3, photo4)
        return render(request, 'virtual_deconstruction_hub/templates_dir/listings/listings_new.html')


