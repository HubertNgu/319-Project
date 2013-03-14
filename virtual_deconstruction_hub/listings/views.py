from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template.defaulttags import csrf_token
from django.template import RequestContext
from django import forms
from listings.models import Listing
from django.shortcuts import render_to_response


def index(request):
#    if request.
    listings_list = Listing.objects.order_by('created')
    context = {'listings_list': listings_list}
    return render(request, 'listings/listings_list.html', context)
#    return render_to_response("listings\listings_list.html",context_instance=RequestContext(request))
#    return render_to_response("listings/listings_list.html", {'listings_list': listings_list},context_instance=RequestContext(request))

def detail(request):
    try:
        listing = Listing.objects.get(pk=listig_id)
    except Listing.DoesNotExist:
        raise Http404
    return render(request, 'listings/listings_individual.html', {'listing': listing} )


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
    
    errormessage = None
    
    if request.method == 'POST':
        
        creator = request.POST.get('creator')
        title = request.POST.get('title')
        textContent = request.POST.get('textContent')
        
        if creator == None:
            errormessage = "You must put in your email"
            return render_to_response("listings/listings_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
        if len(title) < 5:
            errormessage = "Title must be at least 5 characters or long!"
            return render_to_response("listings/listings_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
        if len(textContent) < 5:
            errormessage = "Information on the item must be at least 5 characters or long!"
            return render_to_response("listings/listings_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
        
        try: 
             Listing.objects.get(title = title) 
             errormessage = "There is exactly the same listing created"
             return render_to_response("listings/listings_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
        except:    
            new_listing = Listing(creator = creator, title = title, textContent = textContent)
            new_listing.save()
#            return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
            return   render_to_response("listings/listings_list.html",context_instance=RequestContext(request))
    else:
            return render_to_response("listings/listings_new.html",context_instance=RequestContext(request))


