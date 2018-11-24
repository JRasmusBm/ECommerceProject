from django.shortcuts import render, redirect
from .forms import LoginForm


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect("products:index")
    else:
        form = LoginForm()
    context = {"form": form}
    return render(
        request=request,
        template_name="login_manager/login.html",
        context=context,
    )
