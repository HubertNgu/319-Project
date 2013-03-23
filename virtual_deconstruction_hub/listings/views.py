from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import redirect,get_object_or_404, render_to_response, render
from django.template import Context, loader, RequestContext
from django.template.defaulttags import csrf_token
from django import forms
from listings.models import Listing, ListingForm, EditListingForm
from mailer.models import Email
from mailer.views import send_contact_email
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.sites.models import Site
from mailer.views import send_post_verification_email
import re
import string
import random
from listings.models import Photo
from postpictures.models import UploadForm, PostPictures
import logging

logger = logging.getLogger(__name__)



TEMPLATE_PATHS = {'listings_list': 'listings/listings_list.html',
                  'listings_single': 'listings/listings_individual.html',
                  'listings_new': 'listings/listings_new.html',
                  'listings_success':'listings/new_listing_success.html',
                  'listings_delete': 'listings/listings_delete.html',
                  'listings_edit': 'listings/listings_edit.html'
                  #'listings_upload': 'uploadfile/upload.html',
                  }
URL_PATHS = {'listings_edit-verify': '/listings/edit-verify',
             'listings_delete-verify': '/listings/delete-verify',
             'listings_root': '/listings/',
             'listing_new': '/listing/new'}

MESSAGES = {'verified_listing': "Your listing has been verified and will be displayed on the site. You can make changes to your listing here if you wish.",
            'edit_success': "Your changes have been saved. You can make further changes to your listing if you wish."}


def index(request):
#    if request.
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    listings_list = Listing.objects.filter(verified = True, expired = False).order_by('-created')
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
    return render(request, TEMPLATE_PATHS.get('listings_list'), { "listings" : listings, 'logonparams':logparams })

def detail(request, listing_id):
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    listing = get_object_or_404(Listing, pk=listing_id)
    try:
        listing = Listing.objects.get(id=listing_id)
        address = '%s%%2C+%s' % (str(last_survey.address).replace(' ', '+'), last_survey.city)
    except:
        address = str()
    return render(request, TEMPLATE_PATHS.get('listings_single'), { 'address': address, "listing": listing, 'logonparams':logparams})  
        
def create_listing(request):
    
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    submit_action = '/listings/new'
    pictureform = UploadForm()
    if request.method == 'GET':
        if request.user.is_authenticated():
            form = ListingForm(instance=Listing(), initial={'creator':request.user.email, 'email_verification':request.user.email})
            form.fields['creator'].widget = forms.HiddenInput()
            form.fields['email_verification'].widget = forms.HiddenInput()
        else:
            form = ListingForm(instance=Listing())
        form_args = {'form':form, 'submit_action':submit_action, 'pictureform': pictureform, 'logparams':logparams}
        return render_to_response(TEMPLATE_PATHS.get('listings_new'), form_args, context_instance=RequestContext(request))
    
    if request.method == 'POST':
        listing_form = ListingForm(request.POST)
        form_args = {}
        if request.user.is_authenticated():
            listing_form.fields['creator'].widget = forms.HiddenInput()
            listing_form.fields['email_verification'].widget = forms.HiddenInput()
        if listing_form.is_valid() and request.POST.get("notnewlisting") == None:
            listing = listing_form.save(commit=False)
            listing.url = re.sub(r'\W+', '', listing.title.lower().replace (" ", "_"))
            listing_url = listing.get_url()
            #if user is logged in, then verify post
            if request.user.is_authenticated:
                listing.verified = True
            
            #check that url is unique in db, if url already exists
            # append a random 10 char string to the end
            if Listing.objects.filter(url=listing.url).count() > 0:
                listing.url = tag_maker("_", listing.url + ' ' + random_string_generator(10))
            
            listing_url = listing.url
            listing_url = HttpRequest.build_absolute_uri(request, listing_url)
            
#            if request.user.is_authenticated():
#                listing.verified = True

            listing.save()
            listingid = listing.id
            logger.debug('format', "createListing: debug")
            form = UploadForm(request.POST, request.FILES)
            if request.POST.get("notnewlisting") != None:
                    listingid = request.POST.get("listingid")
                    listing = Listing.objects.get(id = listingid )
                    listing_url = listing.get_url()
            form_args = {'form':listing_form, 'submit_action':submit_action, 'listing_url' : listing_url, 'listing':listing, 'logparams' : logparams}
           
            if form.is_valid():
                form_args = {'listing':listing, 'listing_url': listing_url, 'logparams':logparams}
                photo = Photo(photo = request.FILES['picture'], listing = listing )
                photo.save()            
                if request.POST.get('pictureform') == "1" and request.POST.get("issubmit") != 1:
                    photolist = Photo.objects.filter(listing_id = listing.id)
                    addanotherprevious = list()
                    for o in Photo.objects.filter(listing_id = listing.id): 
                        addanotherprevious.append(o.photo.name)
                
                    form_args = {'form':listing_form, 'submit_action':submit_action, 
                                  'pictureform': pictureform,
                                 'listingid' :listingid, 'addanotherprevious' : addanotherprevious,
                                 'logparams': logparams}
                    
                    return render_to_response("listings/listings_new.html", form_args, context_instance=RequestContext(request))
                      
        if listing.verified:
             # if post is already verified, redirect user to their newly created post
            return redirect("/listings/" + listing.url, context_instance=RequestContext(request))
            
        # create a verification/edit link and send with mailer then direct to success message page
        user_email = listing.get_creator()
        verify_url = '/edit-verify?listing_id=%s&uuid=%s' % (listing.id, listing.get_uuid())
        send_post_verification_email(verify_url, user_email, 'list')
#        multiple_entries_for_testing(50)
                
    return render_to_response(TEMPLATE_PATHS.get('listings_success'), form_args, context_instance=RequestContext(request))    
        

def edit_verify_listing(request):  
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
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

        form_args = {'form':edit_form, 'message': message, 'submit_action': submit_action, 'logparams':logparams, 'listing': listing}
        return render_to_response(TEMPLATE_PATHS.get("listings_edit"), form_args, context_instance=RequestContext(request))

        
    if request.method == 'POST':
        edit_form = EditListingForm(request.POST, instance=listing)
        #if post_form valid, process new post
        if edit_form.is_valid():
            post_url = HttpRequest.build_absolute_uri(request, edit_form.cleaned_data.get('url'))
            edit_form.save()
            # This redirects back to edit form, should change to a render_to_response with a message that edit successful
            #return redirect(post_url,context_instance=RequestContext(request))
            #return render_to_response(post_url,context_instance=RequestContext(request))
            form_args = {'form':edit_form, 'submit_action':submit_action, 'message':MESSAGES.get('edit_success'), 'listing_url': listing_url, 'logparams':logparams}
            return render_to_response(TEMPLATE_PATHS.get("listings_edit"), form_args, context_instance=RequestContext(request))
        else:
            # if form submission not valid, redirect back to form with error messages
            form_args = {'form':edit_form, 'submit_action':submit_action, 'message':None, 'logparams':logparams}
            return render_to_response(TEMPLATE_PATHS.get("listings_edit"), form_args, context_instance=RequestContext(request)) 



def delete_verify_listing(request): 
     
    listing_id = request.GET.get('listing_id')
    uuid = request.GET.get('uuid')
    #action for submit button
    delete_submit_action = URL_PATHS.get('listings_delete-verify') + '?listing_id=' + listing_id + '&uuid=' + uuid
    listing = get_object_or_404(Listing, id=str(listing_id))
    if not listing:
        message = "Listing does not exist or it has already been deleted"
        form_args = { "message" : message }
        return render_to_response(TEMPLATE_PATHS.get("listings_delete"), form_args, context_instance=RequestContext(request))
    else:
        listing.expired = True
        listing.save()
        message = "Listing is successfully deleted"
        form_args = { "message" : message }
        return render_to_response(TEMPLATE_PATHS.get("listings_delete"), form_args, context_instance=RequestContext(request))
    
#    if request.method == 'POST':      
#        if listing.is_verified():   
#            if listing and (listing.get_uuid() == str(uuid)):
#                listing.delete()
#            else:
#                raise Http404
#        
#        form_args = {'listing': listing, 'delete_submit_action': submit_action}
#        return render_to_response(TEMPLATE_PATHS.get("listings_delete"), form_args, context_instance=RequestContext(request))
#         
    

def tag_maker(space_replacement_char, tag_string):
    return re.sub(r'\W+', '', tag_string.lower().replace (" ", space_replacement_char ))

def random_string_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def contact_seller(request, listing_id):
    if request.user.is_authenticated():
        logtext = "Logout"
        accounttext = "My Account"
        welcometext = request.user.username
        logparams=[logtext,accounttext, welcometext]
    else: 
        logtext = "Login"
        accounttext = "Sign Up"
        logparams=[logtext,accounttext]
    submit_action = '/listings/contactSeller/' + listing_id + '/'
    if request.method == 'GET':
        form_args = {'submit_action':submit_action, 'logparams':logparams}
        return render_to_response("listings/contact_seller.html", form_args, context_instance=RequestContext(request))
    if request.method == "POST":
        form_args = {'submit_action':submit_action, 'logparams':logparams}
        listing = Listing.objects.get(pk = listing_id) 
        toemail = [listing.creator]
        fromemail = request.POST.get('emailTxt')
        subject = request.POST.get('emailSubject')
        message = request.POST.get('emailMsg')
        send_contact_email(toemail, fromemail, subject, message)
        return render_to_response('listings/new_listing_success.html', form_args, context_instance=RequestContext(request))
         

def multiple_entries_for_testing(number):
    ## fill in test data in db: writes 100 post objects of same type as whatever new form you are entering
    email = 'tisevelyn@gmail.com'
    title = ' Furniture for sale '
    content = ' - Bah blah blah blahahab labalaba hbaalavhgvsha balobuebfuewbfuebfue jefbuefuewbfuewbfuwefbuwebfuweb fiunbefiuwef uefbuwefbwuefbeufb;efuebf'
    for i in xrange(0,number):
        sale="sell"
        ver=True
        exp=False
        if i%2 == 0:
            sale="want"
        if i%5 == 0:
            ver=False
        if i%7 == 0:
            exp=True
        l = Listing(creator=email, title = str(i) + " - " + title, text_content=content, category = 'wood', for_sale=sale,
                    num = 22, street = 'blah', city = 'Vancouver', zipcode = 'V6T1Z4', verified = ver, expired=exp)
        l.save()
    return

