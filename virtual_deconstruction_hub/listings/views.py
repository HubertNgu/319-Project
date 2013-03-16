from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect,get_object_or_404, render_to_response, render
from django.template import Context, loader, RequestContext
from django.template.defaulttags import csrf_token
from django import forms
from listings.models import Listing, ListingForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
import re


def index(request):
#    if request.
    listings_list = Listing.objects.filter(verified = True).order_by('-created')
    paginator = Paginator(listings_list, 25)
    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        listings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        listings = paginator.page(paginator.num_pages)
#    return render_to_response('listings/listings_list.html', {"listings": listings})
    return render(request, 'listings/listings_list.html', { "listings" : listings })


def detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
#    return render_to_response('listings/listings_individual.html', {'listing': listing })
    return render(request, 'listings/listings_individual.html', {"listing": listing})
    
      

#def searchListing(request):
#    if request.method == 'SEARCH':
#        keyword = request.SEARCH.get('keyword')
#        listings_results = Listing.objects.raw('SELECT * FROM listings WHERE title LIKE %%s%', [keyword])
#        context=Context({
#                     'listings_list' : listings_results,
#                     })
#        return HttpResponse(HttpResponse(template.render(context)))
#
#def filterListing(request, listing_type):
#    if(listing_type == 'Items for sale'):
#        listings_results = Listing.objects.raw('SELECT * FROM listings WHERE type == "Items for sale" ')
#        context=Context({
#                     'listings_list' : listings_results,
#                     })
#        return HttpResponse(HttpResponse(template.render(context)))
#    if(listings_type == 'Wanted items'):
#        listings_results = Listing.objects.raw('SELECT * FROM listings WHERE type == "Wanted Items" ')
#        context=Context({
#                     'listings_list' : listings_results,
#                     })
#        return HttpResponse(HttpResponse(template.render(context)))
        
        
def createListing(request):
    submit_action = '/listings/new'
    if request.method == 'GET':
        form = ListingForm(instance=Listing())
        form_args = {'form':form, 'submit_action':submit_action}
        return render_to_response("listings/listings_new.html", form_args, context_instance=RequestContext(request))
    if request.method == 'POST':
        listing_form = ListingForm(request.POST)
        if listing_form.is_valid():
            listing = listing_form.save(commit=False)
            listing.url = re.sub(r'\W+', '', listing.title.lower().replace (" ", "_"))
            listing_url = listing.url
            listing_url = HttpRequest.build_absolute_uri(request, listing_url)
#            if request.user.is_authenticated():
#                listing.verified = True
            listing.save()
            form_args = {'listing':listing, 'listing_url':listing_url}
            
            if request.GET.get('photo_upload') is 1:
                pass
            
            
#            ## fill in test data in db: writes 100 post objects of same type as whatever new form you are entering
#            email = 'evelyn@testing.com'
#            title = ' Test Title '
#            content = ' - Bah blah blah blahahab labalaba hbaalavhgvsha balobuebfuewbfuebfue jefbuefuewbfuewbfuwefbuwebfuweb fiunbefiuwef uefbuwefbwuefbeufb;efuebf'
#            
#            for i in xrange(0,100):
#                l = Listing(creator=email, title=title+str(i),textContent=str(i)+content, category = 'PARTBD', price = str(i), verified=True)
#                l.save()
            
            
            return render_to_response('listings/new_listing_success.html', form_args, context_instance=RequestContext(request))
        
        else:
            form_args = {'form':listing_form, 'submit_action': submit_action}
            return render_to_response("listings/listings_new.html", form_args, context_instance=RequestContext(request))

#        creator = request.POST.get('creator')
#        title = request.POST.get('title')
#        textContent = request.POST.get('textContent')
#        if creator == None:
#            errormessage = "You must put in your email"
#            return render_to_response("listings/listings_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
#        if len(title) < 5:
#            errormessage = "Title must be at least 5 characters or long!"
#            return render_to_response("listings/listings_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
#        if len(textContent) < 5:
#            errormessage = "Information on the item must be at least 5 characters or long!"
#            return render_to_response("listings/listings_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
#        try: 
#             Listing.objects.get(title = title) 
#             errormessage = "There is exactly the same listing created already"
#             return render_to_response("listings/listings_new.html",{'errormessage':errormessage},context_instance=RequestContext(request))
#        except:    
#            new_listing = Listing(creator = creator, title = title, textContent = textContent)
#            new_listing.verified = False;
#            new_listing.save()
#            return redirect('/listings/')
#    else:
#            return render_to_response("listings/listings_new.html",context_instance=RequestContext(request))

def editListing(request, listing_id):
    
    submit_action = '/listings/edit/' + listing_id + '/'
    listing = Listing.objects.get(pk = listing_id) 
    
    if request.method == 'GET':
        form = ListingForm(instance=listing)
        form_args = {'form':form, 'submit_action':submit_action}
        return render_to_response("listings/listings_new.html", form_args, context_instance=RequestContext(request))
    
    if request.method == "POST":
        listing_form = ListingForm(request.POST, instance = listing)
        if listing_form.is_valid():
            listing = listing_form.save(commit=False)
            listing.url = re.sub(r'\W+', '', listing.title.lower().replace (" ", "_"))
            listing_url = listing.url
            listing_url = HttpRequest.build_absolute_uri(request, listing_url)
#            if request.user.is_authenticated():
#                listing.verified = True
            listing.save()
            form_args = {'listing':listing, 'listing_url':listing_url}
            
            if request.GET.get('photo_upload') is 1:
                pass
        
            return render_to_response('listings/new_listing_success.html', form_args, context_instance=RequestContext(request)) 
        else:
            form_args = {'form':listing_form, 'submit_action': submit_action}
            return render_to_response("listings/listings_new.html", form_args, context_instance=RequestContext(request)) 
        
#        title = request.POST.get('title')
#        textContent = request.POST.get('textContent')
#        listing.title = title
#        listing.textContent = textContent
#        listing.lastModified = timezone.now()
#        listing.save()
#        return redirect('/listings/') 
#    else:
#        creator = listing.creator
#        title = listing.title
#        textContent = listing.textContent
#        return render_to_response("users\editaccount.html",{'creator':creator,'title':title,'textContent':textContent,},
#                                  context_instance=RequestContext(request))

