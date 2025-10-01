from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import UserAccount
from .forms import SignupForm

def signup_save(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # ✅ Save to DB only after verification
            if request.POST.get("is_verified") == "true":
                form.save()
                return redirect("login")  # or success page
            else:
                # valid form, but email not yet verified
                return render(request, "signup.html", {"form": form, "show_modal": True})
        else:
            return render(request, "signup.html", {"form": form})
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})




def login_view(request):
    error = None

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user exists
        user_obj = UserAccount.objects.filter(email=email, password=password).first()

        if user_obj:
            return redirect("dashboard")
        else:
            error = "Invalid email or password!"

    return render(request, "login.html", {"error": error})



