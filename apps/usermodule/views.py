from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register_user")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register_user")

        User.objects.create_user(username=username, password=password)
        messages.success(request, "You have successfully registered")
        return redirect("login_user")

    return render(request, "usermodule/register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully")
            return redirect("/books/students/")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login_user")

    return render(request, "usermodule/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect("login_user")


from django.shortcuts import render

# Create your views here.
