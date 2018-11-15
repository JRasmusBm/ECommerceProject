
from django.shortcuts import render


def index(request):
    context = {"page_title": "Berries"}
    return render(
        request=request,
        template_name="berries/index.html",
        context=context,
    )
