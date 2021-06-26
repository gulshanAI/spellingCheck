from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkIt, name='checkIt'),
]
