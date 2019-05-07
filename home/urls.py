from django.urls import path
import django.views

from home import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name = 'index'),
    
    path('annos/', views.annos, name = 'annos'),

    path('about/', views.about, name = 'about'),
]