from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home', views.index, name='home'),
    path('jeeneet', views.jeeneet, name='jeeneet'),
    path('firstyear', views.firstyear, name='firstyear'),
    path('impques', views.importantquestion, name='impques'),
    path('about', views.about, name='about')
]
