from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def loading(request):
    return render(request, 'frontend/index.html')

def home(request):
    return render(request, 'frontend/home_page.html')