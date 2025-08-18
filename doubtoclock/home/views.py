from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt  # Disable CSRF protection for this view (not recommended for production)
def index(request):
    return render(request, 'index.html')
def jeeneet(request):
    return render(request, 'jeeneet.html')
def firstyear(request):
    return render(request, '1styear.html')
def importantquestion(request):
    return render(request, 'impques.html')
def profilepage(request):
    return render(request, 'profilepage.html')
def about(request):
    return HttpResponse("this is about page") 