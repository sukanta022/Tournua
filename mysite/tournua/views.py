from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import UserAccount
from .forms import SignupForm
from django.views.decorators.cache import never_cache

def signup_save(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
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
            request.session["user_id"] = user_obj.id
            return redirect("dashboard")
        else:
            error = "Invalid email or password!"

    return render(request, "login.html", {"error": error})



@never_cache
def dashboard(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    try:
        user = UserAccount.objects.get(id=user_id)
        name = user.full_name.split(" ")[0]
    except UserAccount.DoesNotExist:
        return redirect("login")

    return render(request, "demo.html", {"name": name})


def logout_view(request):
    # Clear all session data
    request.session.flush()  # This removes all session data
    return redirect("home")






