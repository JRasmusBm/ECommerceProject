from django.shortcuts import render


def index(request):
    context = {"page_title": "About", "user": request.user}
    return render(
        request=request, template_name="about/index.html", context=context
    )
