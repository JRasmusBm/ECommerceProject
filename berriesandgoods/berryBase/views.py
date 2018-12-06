from django.shortcuts import render, redirect

from home.models import Product
from .forms import AddToCartForm
from basket.orders import OrdersBackend


def unpack_product(product):
    return {
        "name": product.nameproduct,
        "price": format(product.priceproduct / 100, ".2f"),
        "unit": product.nameproducttype.unit,
        "product_id": product.idproduct,
        "image": product.img,
    }


def index(request):
    context = {
        "page_title": "Berries",
        "products": [
            unpack_product(product)
            for product in Product.objects.raw("SELECT * FROM product")
        ],
    }
    return render(
        request=request,
        template_name="products/index.html",
        context=context,
    )


def details(request, product_id, message=""):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login:login")
        form = AddToCartForm(request.POST)
        if form.is_valid():
            ordersBackend = OrdersBackend()
            ordersBackend.addProduct(username=request.user.email, productId=product_id, amount=int(form.data["amount"]))
            return redirect("products:details", product_id=product_id)
    else:
        form = AddToCartForm()
    context = {
        "page_title": "Details",
        "product": unpack_product(
            Product.objects.raw(
                f"SELECT * FROM product WHERE idproduct={product_id};"
            )[0]
        ),
        "form": form,
        "message": message,
    }
    return render(
        request=request,
        template_name="products/details.html",
        context=context,
    )
