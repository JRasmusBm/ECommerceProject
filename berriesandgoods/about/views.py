from django.shortcuts import render


def index(request):
    context = {"page_title": "About"}
    return render(
        request=request, template_name="about/index.html", context=context
    )
