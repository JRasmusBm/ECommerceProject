from django.shortcuts import render


def index(request):
    context = {"page_title": "Home"}
    return render(
        request=request, template_name="home/index.html", context=context
    )
