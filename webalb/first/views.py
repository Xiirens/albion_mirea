from django.shortcuts import render

# Create your views here.

def first_page(request):
    return render(request, 'first.html')

def login_page(request):
    return render(request, 'login.html')