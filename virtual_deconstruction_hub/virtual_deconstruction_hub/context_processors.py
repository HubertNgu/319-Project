from django.conf import settings
from django.contrib.sites.models import Site

def current_site(request):
    try:
        current_site = Site.objects.get_current()
        return {
            'current_site': current_site,
            'STATIC_URL': settings.STATIC_URL,
        }
    except Site.DoesNotExist:
        # always return a dict, no matter what!
        return {'current_site':'',
                'STATIC_URL':''} # an empty string