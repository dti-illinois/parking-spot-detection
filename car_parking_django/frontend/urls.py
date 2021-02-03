from django.urls import path
from . import views

urlpatterns = [
    path('', views.loading, name='loading'),
    path(r'home', views.home, name='home')
]
