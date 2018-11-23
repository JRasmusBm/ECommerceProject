from django.shortcuts import render
from home.models import Product


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


def details(request, product_id):
    context = {
        "page_title": "Details",
        "product": unpack_product(
            Product.objects.raw(
                f"SELECT * FROM product WHERE idproduct={product_id};"
            )[0]
        ),
    }
    return render(
        request=request,
        template_name="products/details.html",
        context=context,
    )
