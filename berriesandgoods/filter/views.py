from django.shortcuts import render, redirect
from django.db import connection

from home.models import Product, Review, Users
from .forms import AddToCartForm, EditReviewForm

from .forms import AddToCartForm, EditReviewForm
import logging




 #Unpack the product from
def unpack_product(product):
    return {
        "name": product.nameproduct,
        "price": format(product.priceproduct / 100, ".2f"),
        "unit": product.nameproducttype.unit,
        "idproduct": product.idproduct,
        "image": product.img,
    }


def index(request):
    context = {
        "page_title": "filter",
        "products": [
            unpack_product(product)
            for product in Product.objects.raw("SELECT * FROM product")
        ],
        "user": request.user,
    }
    return render(
        request=request,
        template_name="filter/index.html",
        context=context,
    )

def sort_by_price(request,intervall):
    if intervall == "0-12":
        context = {
        "page_title": "Result",
        "products": [
            unpack_product(product)
            for product in Product.objects.raw("SELECT * FROM product")]


    }
    return render(
        request = request,
        template_name="filter/index.html",
        context = context,
    )


