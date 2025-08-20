from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

def coins():
    return 69
# Create your views here.
@csrf_exempt  # Disable CSRF protection for this view (not recommended for production)
def index(request):
    context = {
            'coins': coins(),
        }
    return render(request, 'index.html', context)
def jeeneet(request):
    context = {
            'coins': coins(),
        }
    return render(request, 'jeeneet.html', context)
def firstyear(request):
    context = {
            'coins': coins(),
        }
    return render(request, '1styear.html', context)
def importantquestion(request):
    context = {
            'coins': coins(),
        }
    return render(request, 'impques.html', context)
def profilepage(request):
    context = {
            'coins': coins(),
        }
    return render(request, 'profilepage.html', context)
def about(request):
    return HttpResponse("this is about page") 