from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CustomUserSignupForm, ImageUploadForm, DoubtForm   # import your form
from .models import DoubtCoinWallet, UserImage # import the coinwallet


def coins(user):
    if user.is_authenticated:
        wallet = get_object_or_404(DoubtCoinWallet, user=user)
        return wallet.balance
    return 0   # not logged in → no coins

# Create your views here.

def index(request):
    context = {
            'coins': coins(request.user),
        }
    return render(request, 'index.html', context)
def jeeneet(request):
    context = {
            'coins': coins(request.user),
        }
    return render(request, 'jeeneet.html', context)
def firstyear(request):
    context = {
            'coins': coins(request.user),
        }
    return render(request, '1styear.html', context)
def importantquestion(request):
    context = {
            'coins': coins(request.user),
        }
    return render(request, 'impques.html', context)

def about(request):
    return HttpResponse("this is about page") 

@login_required(login_url="login")   # If not logged in, redirect to login page
def profilepage(request):
    context = {
            'coins': coins(request.user),
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

def signup(request):
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()     
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")   
            return redirect("login")
        else:
            return render(request,'signup.html', {"form": form, 'error':form.errors})  # ✅ see validation errors in terminal 
    else:
        form = CustomUserSignupForm()
    return render(request, "signup.html", {"form": form})



def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Image is uploaded to Cloudinary, URL saved in MySQL
            return redirect("gallery")
    else:
        form = ImageUploadForm()
    return render(request, "upload.html", {"form": form})

def gallery(request):
    images = UserImage.objects.all()
    return render(request, "gallery.html", {"images": images})    

def ask_doubt(request):
    if request.method == "POST":
        form = DoubtForm(request.POST)
        if form.is_valid():
            doubt = form.save(commit=False)
            doubt.user = request.user  # link doubt with logged-in user
            doubt.save()
            return redirect('home')
    else:
        form = DoubtForm()
    return render(request, 'ask_doubt.html', {'form': form})

# TODO Make an about page