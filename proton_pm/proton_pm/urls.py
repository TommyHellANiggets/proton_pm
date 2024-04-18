from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('main', include('myapp.urls')),
    path('terminal', include('myapp.urls')),
    path('load_photo', include('myapp.urls')),
    path('profile', include('myapp.urls')),

]
