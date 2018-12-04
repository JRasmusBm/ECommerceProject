from django.shortcuts import redirect


def index(request):
    return redirect("products:index")
