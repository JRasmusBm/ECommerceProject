from django.shortcuts import render
from django.contrib.auth.middleware import AuthenticationMiddleware

from .orders import OrdersBackend
from login_manager.views import login_screen
    
    
def unpack_product(product):
    return {
        "name": product.nameproduct,
        "price": format(product.priceproduct / 100, ".2f"),
        "unit": product.nameproducttype.unit,
        "product_id": product.idproduct,
        "image": product.img,
    }

def index(request):
    ordersBackend = OrdersBackend()
    user = request.user
    if not request.user.is_authenticated:
        login_screen
        user = request.user
    order = ordersBackend.getOrder(user.email)
    get = ordersBackend.getProducts(order.idorders)
    if len(get) > 1:
        products = get[1]
        orderProducts = get[0]
        products.sort(key=lambda x: x.idproduct)
        orderProducts.order_by("idproduct")
    else:
        products = []
        orderProducts = []
    context = {
        "page_title": "Basket",
        "products":[
            unpack_product(product)
            for product in products
        ],
        "orderProducts":orderProducts
    }
    return render(
        request=request, template_name="basket/index.html", context=context
    )
