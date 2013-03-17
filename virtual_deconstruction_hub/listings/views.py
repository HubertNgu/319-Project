from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect,get_object_or_404, render_to_response, render
from django.template import Context, loader, RequestContext
from django.template.defaulttags import csrf_token
from django import forms
from listings.models import Listing, ListingForm, EditListingForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.sites.models import Site
from mailer.views import send_post_verification_email
import re
import string
import random

TEMPLATE_PATHS = {'listings_list': 'listings/listings_list.html',
                  'listings_single': 'listings/listings_individual.html',
                  'listings_new': 'listings/listings_new.html',
                  'listings_success':'listings/new_listing_success.html'
                  #'listings_upload': 'uploadfile/upload.html',
                  }
URL_PATHS = {'listings_edit-verify': '/listings/edit-verify',
             'listings_root': '/listings/',
             'listing_new': '/listing/new'}

MESSAGES = {'verified_listing': "Your listing has been verified and will be displayed on the site. You can make changes to your listing here if you wish.",
            'edit_success': "Your changes have been saved. You can make further changes to your listing if you wish."}


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
    return render(request, TEMPLATE_PATHS.get('listings_list'), { "listings" : listings })


def detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, TEMPLATE_PATHS.get('listings_single'), {"listing": listing})  

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
        return render_to_response(TEMPLATE_PATHS.get('listings_new'), form_args, context_instance=RequestContext(request))
    if request.method == 'POST':
        listing_form = ListingForm(request.POST)
        if listing_form.is_valid():
            listing = listing_form.save(commit=False)
            listing.url = re.sub(r'\W+', '', listing.title.lower().replace (" ", "_"))
            listing_url = listing.url
            #check that url is unique in db, if url already exists
            # append a random 10 char string to the end
            if Listing.objects.filter(url=listing.url).count() > 0:
                listing.url = tag_maker("_", listing.url + ' ' + random_string_generator(10))
            
            listing_url = listing.url
            listing_url = HttpRequest.build_absolute_uri(request, listing_url)
            
#            if request.user.is_authenticated():
#                listing.verified = True
            listing.save()
            form_args = {'listing':listing, 'listing_url':listing_url}
            
            if request.GET.get('photo_upload') is 1:
                pass
                      
            if listing.verified:
                # if post is already verified, redirect user to their newly created post
                return redirect(listing.url, context_instance=RequestContext(request))
            
             # create a verification/edit link and send with mailer then direct to success message page
            user_email = listing.get_creator()
            verify_url = '%s/edit-verify?listing_id=%s&uuid=%s' % (Site.objects.get_current(), listing.id, listing.get_uuid())
            send_post_verification_email(verify_url, user_email, 'list')
            
            return render_to_response(TEMPLATE_PATHS.get('listings_success'), form_args, context_instance=RequestContext(request))
        
        else:
            form_args = {'form':listing_form, 'submit_action': submit_action}
            return render_to_response(TEMPLATE_PATHS.get('listings_new'), form_args, context_instance=RequestContext(request))

def edit_verify_listing(request):  
    listing_id = request.GET.get('listing_id')
    uuid = request.GET.get('uuid')
    #action for submit button
    submit_action = URL_PATHS.get('listings_edit-verify') + '?listing_id=' + listing_id + '&uuid=' + uuid
    listing_url = None
    listing = None
    message = None
    try:
        listing = get_object_or_404(Listing, id=str(listing_id))
    except:
        raise Http404
        
    if request.method == 'GET':      
        if not listing.is_verified():   
            if listing and (listing.get_uuid() == str(uuid)):
                listing.mark_verified()
                listing.save()
                message = MESSAGES.get('verified_listing')
#                post_url = HttpRequest.build_absolute_uri(request, listing.get_url())
#                return redirect(post_url,context_instance=RequestContext(request))
            else:
                # the listing_id and uuid provided do not match anything in db correctly
                # so redirect to 404 as this page doesn't exist for this combination
                raise Http404
        #post verified by this point, render edit page with message
        edit_form = EditListingForm(instance=listing)
        form_args = {'form':edit_form, 'message': message, 'submit_action': submit_action}
        return render_to_response(TEMPLATE_PATHS.get("listings_new"), form_args, context_instance=RequestContext(request))
        
    if request.method == 'POST':
        edit_form = EditListingForm(request.POST, instance=listing)
        #if post_form valid, process new post
        if edit_form.is_valid():
            post_url = HttpRequest.build_absolute_uri(request, edit_form.cleaned_data.get('url'))
            edit_form.save()
            # This redirects back to edit form, should change to a render_to_response with a message that edit successful
            #return redirect(post_url,context_instance=RequestContext(request))
            #return render_to_response(post_url,context_instance=RequestContext(request))
            form_args = {'form':edit_form, 'submit_action':submit_action, 'message':MESSAGES.get('edit_success'), 'listing_url': listing_url}
            return render_to_response(TEMPLATE_PATHS.get("listings_new"), form_args, context_instance=RequestContext(request))
        else:
            # if form submission not valid, redirect back to form with error messages
            form_args = {'form':edit_form, 'submit_action':submit_action, 'message':None}
            return render_to_response(TEMPLATE_PATHS.get("listings_new"), form_args, context_instance=RequestContext(request)) 

def tag_maker(space_replacement_char, tag_string):
    return re.sub(r'\W+', '', tag_string.lower().replace (" ", space_replacement_char ))

def random_string_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

