# pages/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('text-to-speech', views.textToSpeech, name='text_to_speech'),
    path('about/', views.aboutPageView, name='about'),
]