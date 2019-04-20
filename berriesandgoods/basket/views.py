from django.shortcuts import render, redirect

from .orders import ordersBackend
from .forms import ChangeAmount

from view_orders.views import unpack_product, unpack_order


def removeProduct(request, idproduct):
    if not request.user.is_authenticated:
        return redirect("login:login")
    ordersBackend.removeProduct(user=request.user, idproduct=idproduct)
    return redirect("basket:index")


def changeAmount(request, idproduct):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login:login")
        formChange = ChangeAmount(request.POST)
        if formChange.is_valid():
            ordersBackend.changeAmount(
                idproduct=idproduct,
                user=request.user,
                amount=int(formChange.data["amount"]),
            )
    return redirect("basket:index")


def checkout(request):
    if not request.user.is_authenticated:
        return redirect("/")
    ordersBackend.pay(user=request.user)
    return redirect("basket:index")


def index(request):
    if not request.user.is_authenticated:
        return redirect("login:login")
    order = ordersBackend.getOrCreateOrder(user=request.user)
    price = order.price
    formChange = ChangeAmount(auto_id=False)
    products = [
        unpack_product(product=product, orderItem=orderItem)
        for product, orderItem in ordersBackend.getProducts(
            idorders=order.idorders
        )
    ]
    context = {
        "page_title": "Basket",
        "products": products,
        "priceorder": format(price / 100, ".2f"),
        "formChange": formChange,
        "user": request.user,
        "order": unpack_order(order=order, user=request.user),
    }
    return render(
        request=request, template_name="basket/index.html", context=context
    )
