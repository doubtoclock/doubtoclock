from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CustomUserSignupForm, ImageUploadForm, DoubtForm_jn, DoubtForm_fy   # import your form
from .models import DoubtCoinWallet, UserImage, Doubt_jn, Doubt_fy # import the coinwallet
from django.http import JsonResponse



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
    doubts = Doubt_jn.objects.all().order_by('-created_at')
    context = {
            'coins': coins(request.user),
            'doubts': doubts
        }
    return render(request, 'jeeneet.html', context)

def firstyear(request):
    doubts = Doubt_fy.objects.all().order_by('-created_at')
    context = {
            'coins': coins(request.user),
            'doubts': doubts
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

@csrf_exempt
def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        img = request.FILES["image"]
        title = request.POST.get("title", img.name)
        obj = UserImage(title=title, image=img)
        obj.save()  # important — triggers Cloudinary upload
        return JsonResponse({"url": obj.image.url})
    return JsonResponse({"error": "No file uploaded"}, status=400)
    
def gallery(request):
    images = UserImage.objects.all()
    return render(request, "gallery.html", {"images": images})    


@login_required(login_url='login')  # redirect to your login page if not logged in
def ask_doubt_jn(request):
    if request.method == "POST":
        form = DoubtForm_jn(request.POST)
        if form.is_valid():
            doubt = form.save(commit=False)
            doubt.user = request.user
            doubt.save()
            return redirect('jeeneet')
    else:
        form = DoubtForm_jn()
    return render(request, 'index.html', {'form': form})

@login_required(login_url='login')  # redirect to your login page if not logged in
def ask_doubt_fy(request):
    if request.method == "POST":
        form = DoubtForm_fy(request.POST)
        if form.is_valid():
            doubt = form.save(commit=False)
            doubt.user = request.user
            doubt.save()
            return redirect('firstyear')
    else:
        form = DoubtForm_fy()
    return render(request, 'index.html', {'form': form})

@login_required(login_url='login')
def editprofile(request):
    profile = request.user.profile
    context = {
            'coins': coins(request.user),
        }
    if request.method == "POST":
        selected_pic = request.POST.get('profile_pic')
        if selected_pic:
            # extract number (1–8) from filename
            profile.random_number = int(selected_pic.split('.')[0])
            profile.save()
        return redirect('profilepage')
    return render(request, 'editprofile.html', context)