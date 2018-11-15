from django.shortcuts import render


def index(request):
    berries = [
        {
            "name": "Berry1"
        },
        {
            "name": "Berry2"
        },
        {
            "name": "Berry3"
        },
    ]
    context = {"page_title": "Berries", "berries": berries}
    return render(
        request=request,
        template_name="berries/index.html",
        context=context,
    )
