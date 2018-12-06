from django.shortcuts import render, redirect
from django.contrib.auth.middleware import AuthenticationMiddleware

from .orders import OrdersBackend
from .forms import ChangeAmount
from login_manager.views import login_screen
from home.models import Orders
    

def removeProduct(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login:login")
    ordersBackend = OrdersBackend()
    ordersBackend.removeProduct(productId= product_id)
    return redirect('basket:index')

def changeAmount(request, product_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login:login")
        formChange = ChangeAmount(request.POST)
        if formChange.is_valid():
            ordersBackend = OrdersBackend()
            ordersBackend.changeAmount(productId=product_id, amount=int(formChange.data["amount"]))
    return redirect("basket:index")

def checkout(request):
    if not request.user.is_authenticated:
        return redirect("/")
    user = request.user
    ordersBackend = OrdersBackend()
    ordersBackend.pay(user.idusers)
    return redirect("basket:index")

def unpack_product(product, orderItem):
    return {
        "name": product.nameproduct,
        "price": format(product.priceproduct / 100, ".2f"),
        "unit": product.nameproducttype.unit,
        "product_id": product.idproduct,
        "image": product.img,
        "amount": format(orderItem.amount),
        "orderprice": format((orderItem.priceorderitems * orderItem.amount) / 100, ".2f"),
        "orderitem_id": orderItem.idorderitems,
    }

def index(request):
    ordersBackend = OrdersBackend()
    user = request.user
    order = Orders.objects.filter(idusers=user.idusers)
    order = order.filter(payment=False)
    if order.exists():
        order = order.get()
        price = order.price
    formChange = ChangeAmount(auto_id=False)
    if not request.user.is_authenticated:
        login_screen
        user = request.user
    order = ordersBackend.getOrder(user.email)
    get = ordersBackend.getProducts(order.idorders)
    if len(get) > 1:
        get[0].sort(key=lambda x: x.idproduct)
        get[1].sort(key=lambda x: x.idproduct.idproduct)
    else:
        get=[[],[]]
    get = [
        unpack_product(product, orderItem)
        for product, orderItem in zip(get[0], get[1])
    ]
    context = {
        "page_title" : "Basket",
        "products" : get,
        "priceorder" : format(price / 100, ".2f"),
        "formChange" : formChange,
    }
    return render(
        request=request, template_name="basket/index.html", context=context
    )
