from django.contrib import admin
from django.urls import path, include
from home import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='home'),
    path('home', views.index, name='home'),
    path('jeeneet', views.jeeneet, name='jeeneet'),
    path('firstyear', views.firstyear, name='firstyear'),
    path('impques', views.importantquestion, name='impques'),
    path('profilepage', views.profilepage, name='profilepage'),
    path('about', views.about, name='about'),
    path('login', views.login_view, name="login"),
    path('signup', views.signup, name="signup"),

    # ✅ Edited: added next_page so logout redirects instead of white screen
    path("accounts/logout/", LogoutView.as_view(next_page="/"), name="account_logout"),

    path('accounts/', include('allauth.urls')),
]