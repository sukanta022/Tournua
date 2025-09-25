from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import UserAccount


def signup_save(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        print("Full Name:", full_name)
        print("Email:", email)
        print("Password:", password)

        # Save data into model
        user = UserAccount(full_name=full_name, email=email, password=password)
        user.save()

        return redirect("login")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = UserAccount.objects.filter(email=email, password=password)
        if user_obj:
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Email not found!"})

    return render(request, "login.html")


