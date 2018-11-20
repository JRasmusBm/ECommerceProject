from django.shortcuts import render
from home.models import Berry

items = [
    {
        "name": berry.nameberry,
        "price": format(round(0.20 + (0.20 * (i % 5)), 2), ".2f"),
        "unit": "kg",
        "item_id": berry.idberry,
    }
    for i, berry in enumerate(Berry.objects.raw("SELECT * FROM berry"))
]


def index(request):
    context = {"page_title": "Berries", "items": items}
    return render(
        request=request, template_name="berries/index.html", context=context
    )


def details(request, item_id):
    context = {
        "page_title": "Details",
        "item": Berry.objects.raw(
            f"SELECT * FROM berry WHERE idBerry={item_id}"
        )[0],
    }
    return render(
        request=request,
        template_name="berries/details.html",
        context=context,
    )
