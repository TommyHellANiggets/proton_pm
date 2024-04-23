from django.contrib import admin
from django.urls import path
from myapp import views


app_name = 'myapp'  # Добавьте эту строку

urlpatterns = [
    path('', views.main, name='main'),
    path('main', views.home, name='home'),
    path('terminal', views.terminal, name='terminal'),
    path('load_photo', views.load_photo, name='load_photo'),
    path('profile', views.profile, name='profile'),
    path('authorization', views.authorization, name='authorization'),
    path('terminal_hello', views.terminal_hello, name='terminal_hello'),
    path('terminal_menu', views.terminal_menu, name='terminal_menu'),
    path('terminal_career', views.terminal_career, name='terminal_career'),
]
