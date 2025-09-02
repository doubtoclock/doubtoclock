from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

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

@login_required(login_url="login")   # If not logged in, redirect to login page
def login(request):
    return render(request, "profilepage.html")  # Your existing profile page