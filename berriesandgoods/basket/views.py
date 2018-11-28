from django.shortcuts import render


def index(request):
    context = {"page_title": "Basket"}
    return render(
        request=request, template_name="basket/index.html", context=context
    )