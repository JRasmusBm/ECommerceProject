from django.shortcuts import render, redirect

from basket.orders import ordersBackend
from login_manager.views import login_screen
from home.models import Orders


def unpack_order(order, user):
    return {
        "id": format(order.idorders),
        "email": order.idusers.email,
        "price": format(order.price / 100, ".2f"),
        "payment": "Paid" if order.payment else "Not Paid",
        "paymentBool": order.payment,
        "status": "Handeled" if order.status else "Not Handeled",
        "statusBool": order.status,
        "is_empty": ordersBackend.isEmpty(order=order),
    }


def unpack_product(product, orderItem):
    return {
        "name": product.nameproduct,
        "price": format(product.priceproduct / 100, ".2f"),
        "unit": product.nameproducttype.unit,
        "idproduct": product.idproduct,
        "image": product.img,
        "amount": format(orderItem.amount),
        "orderprice": format(
            (orderItem.priceorderitems * orderItem.amount) / 100, ".2f"
        ),
        "orderitem_id": orderItem.idorderitems,
    }


def removeOrder(request, idorders):
    if not request.user.is_authenticated:
        return redirect("/")
    if (
        not Orders.objects.filter(idorders=idorders).exists()
        or Orders.objects.get(idorders=idorders).idusers != request.user
    ):
        return redirect("/")
    ordersBackend.removeOrder(idorders=idorders)
    return redirect("view_orders:index")


def removeOrderAdmin(request, idorders):
    if not request.user.admin:
        return redirect("/")
    ordersBackend.removeOrder(idorders=idorders)
    return redirect("view_orders:admin")


def handleOrder(request, idorders):
    if not request.user.is_authenticated or not request.user.admin:
        return redirect("/")
    ordersBackend.handle(idorders)
    return redirect("view_orders:admin")


def orderDetail(request, idorders):
    if not request.user.is_authenticated or not request.user.admin:
        if (
            not Orders.objects.filter(idorders=idorders).exists()
            or Orders.objects.get(idorders=idorders).idusers != request.user
        ):
            return redirect("/")
    order = Orders.objects.get(idorders=idorders)
    orderItems = [
        unpack_product(product, orderItem)
        for product, orderItem in ordersBackend.getProducts(idorders)
    ]
    context = {
        "page_title": "Details Order " + str(order.idorders),
        "order": unpack_order(order, request.user),
        "products": orderItems,
    }
    return render(
        request=request,
        template_name="view_orders/detail.html",
        context=context,
    )


def admin(request):
    if not request.user.is_authenticated or not request.user.admin:
        return redirect("/")
    user = request.user
    orders = Orders.objects.all().order_by("idorders")
    allOrders = []
    for order in orders:
        allOrders.append(order)
    context = {
        "page_title": "View Orders",
        "orders": [unpack_order(order, user) for order in orders],
    }
    return render(
        request=request,
        template_name="view_orders/admin.html",
        context=context,
    )


def index(request):
    if not request.user.is_authenticated:
        login_screen
    user = request.user
    orders = ordersBackend.getOrders(user)
    context = {
        "page_title": "Basket",
        "orders": [unpack_order(order, user) for order in orders],
    }
    return render(
        request=request,
        template_name="view_orders/index.html",
        context=context,
    )
