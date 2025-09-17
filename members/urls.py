from django.urls import path, include
from . import views

APP_NAME = 'members'


urlpatterns = [
    path('', views.home, name='home'),
    path('members/', views.members, name='members'),
    path('details/<slug:slug>', views.details, name='details'),
    path('about/', views.about, name='about'),

]
