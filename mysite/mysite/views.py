from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def signUp(request):
    return render(request, 'signup.html')