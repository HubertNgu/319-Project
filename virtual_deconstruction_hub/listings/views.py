from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from listings.models import Listing


def index(request):
    listings_list = Listing.objects.order_by('created')   
    context = {'listings_list': listings_list}
    return render(request, 'virtual_deconstruction_hub/templates_dir/listings/listings_list.html', context)

def detail(request, listing_id): 
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        raise Http404
    return render(request, 'virtual_deconstruction_hub/templates_dir/listings/listings_individual.html')

def searchListing(request, keyword):
    listings_results = Listing.objects.raw('SELECT * FROM listings WHERE title LIKE %%s%', [keyword])
    context=Context({
                     'listings_list' : listings_results,
                     })
    return HttpResponse(HttpResponse(template.render(context)))

def createListing():
    if request.method == 'POST':
        form = ListingForm(request.POST)
        creator = request.POST.get('creator')
        title = request.POST.get('title')
        textContext = request.POST.get('textContext')
        photo1 = request.POST.get('photo1')
        photo2 = request.POST.get('photo2')
        photo3 = request.POST.get('photo2')
        photo4 = request.POST.get('photo2')
        new_listing = Listing.object.create_listing(cls, creator, title, textContext, 
                                                    photo1, photo2, photo3, photo4)
        new_listing = form.save()
        return redirect('virtual_deconstruction_hub.listings.views.index')




