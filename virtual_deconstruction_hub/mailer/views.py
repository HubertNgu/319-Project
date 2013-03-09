from django.http import HttpResponse

# Create your views here.
def testemail(request):
    if request.is_ajax:
		response = HttpResponse("<p>Here's the text of the Web page.</p>")
		return response
    else:
		return HttpRequest(status=400)