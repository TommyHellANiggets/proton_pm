from django.contrib import admin
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='terminal_hello'),
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('terminal', views.terminal, name='terminal'),
    path('load_photo', views.load_photo, name='load_photo'),
    path('profile', views.profile, name='profile'),
    path('authorization', views.authorization, name='authorization'),
    path('pages', views.pages, name='pages'),
    path('terminal_menu', views.terminal_menu, name='terminal_menu'),
    path('terminal_career', views.terminal_career, name='terminal_career'),
    path('pages/<int:content_id>/', views.content_detail, name='content_detail'),
    path('edit_child/<int:child_id>/', views.edit_child, name='edit_child'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)