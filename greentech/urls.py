from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_post, name='add_post'),
    path('signup/', views.signup, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]
