from django.shortcuts import render, redirect
from .forms import LoginForm, CreateUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def login_screen(request, message=""):
    if request.user.is_authenticated:
        return redirect("home:index")
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home:index")
        else:
            return redirect("login:login", message="Unsuccessful login!")
    else:
        form = LoginForm()
        context = {"form": form, "message": message, "user": request.user}
    return render(
        request=request,
        template_name="login_manager/login.html",
        context=context,
    )


def new_user(request):
    if request.user.is_authenticated:
        return redirect("home:index")
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login:login")
    else:
        form = CreateUserForm()
    context = {"form": form, "user": request.user}
    return render(
        request=request,
        template_name="login_manager/create_user.html",
        context=context,
    )


def log_out(request):
    logout(request)
    return redirect("home:index")
