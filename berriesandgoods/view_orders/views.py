from django.shortcuts import render, redirect

from basket.orders import OrdersBackend
from login_manager.views import login_screen
from home.models import Orders



def removeOrder(request, idorders):
    if not request.user.is_authenticated:
            return redirect("/")
    if Orders.objects.get(idorders=idorders).idusers != request.user:
            return redirect("/")
    ordersBackend = OrdersBackend()
    ordersBackend.removeOrder(idorders=idorders)
    return redirect("view_orders:index")

def removeOrderAdmin(request, idorders):
    if not request.user.admin:
        return redirect("/")
    ordersBackend = OrdersBackend()
    ordersBackend.removeOrder(idorders=idorders)
    return redirect("view_orders:admin")
    
def handleOrder(request, idorders):
    if not request.user.is_authenticated or not request.user.admin:
        return redirect("/")
    ordersBackend = OrdersBackend()
    ordersBackend.handle(idorders)
    return redirect("view_orders:admin")


def unpack_order(order, user):
    ordersBackend = OrdersBackend()
    return {
        "id": format(order.idorders),
        "email" : order.idusers.email,
        "price": format(order.price / 100, ".2f"),
        "payment": ordersBackend.getPaid(order.idorders),
        "paymentBool" : order.payment,
        "status": ordersBackend.getHandeled(order.idorders),
        "statusBool": order.status,
    }

def unpack_orderitem(orderItem):
    return {

    }

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
        "orders": [
            unpack_order(order, user)
            for order in orders
        ],
    }
    return render(
        request=request, template_name="view_orders/admin.html", context=context
    )
    
    

def index(request):
    if not request.user.is_authenticated:
        login_screen
    ordersBackend = OrdersBackend()
    user = request.user
    orders = ordersBackend.getOrders(user)
    context = {
        "page_title": "Basket",
        "orders": [
            unpack_order(order, user)
            for order in orders
        ],
    }
    return render(
        request=request, template_name="view_orders/index.html", context=context
    )
