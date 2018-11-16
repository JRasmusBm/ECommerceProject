from django.shortcuts import render

items = [{
    "name": f"Berry{i}",
    "price": format(round(0.20 + (0.20 * (i % 5)), 2), ".2f"),
    "unit": "kg",
    "item_id": i
} for i in range(100)]


def index(request):
    context = {"page_title": "Berries", "items": items}
    return render(
        request=request,
        template_name="berries/index.html",
        context=context,
    )


def details(request, item_id):
    context = {"page_title": "Details", "item": items[item_id]}
    return render(
        request=request,
        template_name="berries/details.html",
        context=context,
    )
