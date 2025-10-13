from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import CustomUserSignupForm, ImageUploadForm, DoubtForm_jn, DoubtForm_fy
from .models import DoubtCoinWallet, UserImage, Doubt_jn, Doubt_fy


# 🪙 Helper: get user's coin balance
def coins(user):
    if user.is_authenticated:
        wallet = get_object_or_404(DoubtCoinWallet, user=user)
        return wallet.balance
    return 0


# ----------------- BASIC PAGES -----------------
def index(request):
    context = {'coins': coins(request.user)}
    return render(request, 'index.html', context)

def jeeneet(request):
    doubts = Doubt_jn.objects.all().order_by('-created_at')[:5]
    context = {'coins': coins(request.user), 'doubts': doubts}
    return render(request, 'jeeneet.html', context)

def firstyear(request):
    doubts = Doubt_fy.objects.all().order_by('-created_at')[:5]
    context = {'coins': coins(request.user), 'doubts': doubts}
    return render(request, '1styear.html', context)

def importantquestion(request):
    context = {'coins': coins(request.user)}
    return render(request, 'impques.html', context)

def about(request):
    return HttpResponse("this is about page") 


# ----------------- USER AUTH -----------------
@login_required(login_url="login")
def profilepage(request):
    context = {'coins': coins(request.user)}
    return render(request, 'profilepage.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('profilepage')
            else:
                return render(request, 'login.html', {'error': 'Please verify your email before logging in.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, "login.html")


# ----------------- SIGNUP WITH EMAIL VERIFICATION -----------------
def signup(request):
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # ✅ user inactive until verified
            user.save()

            send_verification_email(request, user)

            messages.success(request, "✅ Signup successful! Please check your email to verify your account.")
            return redirect("login")
        else:
            return render(request, 'signup.html', {"form": form, 'error': form.errors})
    else:
        form = CustomUserSignupForm()
    return render(request, "signup.html", {"form": form})


# 📧 Send email verification link
def send_verification_email(request, user):
    from django.core.mail import send_mail
    from django.contrib.sites.shortcuts import get_current_site
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    from django.contrib.auth.tokens import default_token_generator

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain

    verification_link = f"http://{domain}/activate/{uid}/{token}"

    subject = "Verify your email - Your Website Name"
    message = f"""
        Hi {user.username},

        Thank you for signing up at Our Website!

        Please click the link below to verify your email address and activate your account:
        {verification_link}

        If you didn’t request this, you can ignore this email.

        Best,
        Your Website Team
        """

    send_mail(subject, message, 'no-reply@yourwebsite.com', [user.email])

# ✅ Activate user after clicking the link
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "🎉 Your account has been activated! You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Invalid or expired activation link.")
        return redirect('signup')


# ----------------- IMAGE UPLOAD -----------------
@csrf_exempt
def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        img = request.FILES["image"]
        title = request.POST.get("title", img.name)
        obj = UserImage(title=title, image=img)
        obj.save()
        return JsonResponse({"url": obj.image.url})
    return JsonResponse({"error": "No file uploaded"}, status=400)


def gallery(request):
    images = UserImage.objects.all()
    return render(request, "gallery.html", {"images": images})    


# ----------------- DOUBTS -----------------
@login_required(login_url='login')
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


@login_required(login_url='login')
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


# ----------------- PROFILE EDIT -----------------
@login_required(login_url='login')
def editprofile(request):
    profile = request.user.profile
    context = {'coins': coins(request.user)}

    if request.method == "POST":
        selected_pic = request.POST.get('profile_pic')
        if selected_pic:
            profile.random_number = int(selected_pic.split('.')[0])
            profile.save()
        return redirect('profilepage')

    return render(request, 'editprofile.html', context)
