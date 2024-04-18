from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('main', views.home, name='home'),
    path('terminal', views.terminal, name='terminal'),
    path('load_photo', views.load_photo, name='load_photo'),
    path('profile', views.profile, name='profile'),
    
]
