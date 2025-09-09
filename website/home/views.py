from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

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

def about(request):
    return HttpResponse("this is about page") 

@login_required(login_url="login")   # If not logged in, redirect to login page
def profilepage(request):
    context = {
            'coins': coins(),
        }
    return render(request, 'profilepage.html', context)

def login_view(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('profilepage')
        else:
            return render(request,'login.html', {'error':'Invalid username or password'})
    return render(request,"login.html")