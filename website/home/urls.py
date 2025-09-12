from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home', views.index, name='home'),
    path('jeeneet', views.jeeneet, name='jeeneet'),
    path('firstyear', views.firstyear, name='firstyear'),
    path('impques', views.importantquestion, name='impques'),
    path('profilepage', views.profilepage, name = 'profilepage'),
    path('about', views.about, name='about'),
    path('login', views.login_view, name="login"),
    path('signup', views.signup, name="signup"),
    path('accounts/',include('allauth.urls'))

]



