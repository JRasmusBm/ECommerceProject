from django.shortcuts import render, redirect
from django.db import connection

from home.models import Product, Review, Users
from .forms import AddToCartForm, EditReviewForm, SearchForm


def unpack_product(product):
    return {
        "name": product.nameproduct,
        "price": format(product.priceproduct / 100, ".2f"),
        "unit": product.nameproducttype.unit,
        "idproduct": product.idproduct,
        "image": product.img,
    }


def unpack_review(review):
    user = Users.objects.raw(
        "SELECT * FROM users WHERE idusers=%s", [review.idusers.idusers]
    )[0]
    return {
        "user": user.display_name
        if user.display_name not in ["", None]
        else user.email,
        "comment": review.comment,
        "rating": review.rating,
    }


def index(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            return redirect("products:search", term=request.POST["search"])
    search_form = SearchForm()
    context = {
        "search_form": search_form,
        "page_title": "Berries",
        "products": [
            unpack_product(product)
            for product in Product.objects.raw("SELECT * FROM product")
        ],
        "user": request.user,
    }
    return render(
        request=request,
        template_name="products/index.html",
        context=context,
    )


def search(request, term):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            return redirect("products:search", term=request.POST["search"])
    search_form = SearchForm()
    context = {
        "page_title": "Berries",
        "search_form": search_form,
        "products": [
            unpack_product(product)
            for product in Product.objects.raw(
                """SELECT * FROM product
                WHERE ((nameproduct <-> %s) < 0.8
                   OR (nameproducttype <-> %s) < 0.8)
                   ORDER BY (nameproduct <-> %s);""",
                3 * [term],
            )
        ],
        "user": request.user,
    }
    return render(
        request=request,
        template_name="products/index.html",
        context=context,
    )


def edit_reviews(request, idproduct):
    if not request.user.is_authenticated:
        return redirect("login:login")
    if request.method == "POST":
        form = EditReviewForm(request.POST)
        if form.is_valid():
            comment = request.POST["comment"]
            rating = request.POST["rating"]
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO review (idusers, idproduct, comment, rating)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (idusers, idproduct)
                    DO UPDATE
                        SET comment = %s, rating = %s;""",
                    [
                        request.user.idusers,
                        idproduct,
                        comment,
                        rating,
                        comment,
                        rating,
                    ],
                )
            return redirect("products:reviews", idproduct=idproduct)
    else:
        form = EditReviewForm()
    context = {
        "page_title": "Reviews",
        "product": unpack_product(
            Product.objects.raw(
                "SELECT * FROM product WHERE idproduct=%s;", [idproduct]
            )[0]
        ),
        "old_review": Review.objects.raw(
            """SELECT * FROM review WHERE
                                 idproduct={idproduct} AND
                                 idusers={request.user.idusers}"""
        ),
        "form": form,
    }
    return render(
        request=request,
        template_name="products/edit_reviews.html",
        context=context,
    )


def reviews(request, idproduct):
    reviews = Review.objects.raw(
        "SELECT * FROM review WHERE idproduct=%s;", [idproduct]
    )
    context = {
        "page_title": "Reviews",
        "product": unpack_product(
            Product.objects.raw(
                "SELECT * FROM product WHERE idproduct=%s;", [idproduct]
            )[0]
        ),
        "reviewAmount": len(reviews),
        "reviewScore": sum(review.rating for review in reviews)
        / len(reviews)
        if len(reviews) > 0
        else 0,
        "reviews": [unpack_review(review) for review in reviews],
    }
    return render(
        request=request,
        template_name="products/reviews.html",
        context=context,
    )


def details(request, idproduct, message=""):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login:login")
        form = AddToCartForm(request.POST)
        if form.is_valid():
            return redirect("products:details", idproduct=idproduct)
    else:
        form = AddToCartForm()
    reviews = Review.objects.raw(
        "SELECT * FROM review WHERE idproduct=%s;", [idproduct]
    )
    context = {
        "page_title": "Details",
        "product": unpack_product(
            Product.objects.raw(
                "SELECT * FROM product WHERE idproduct=%s;", [idproduct]
            )[0]
        ),
        "form": form,
        "message": message,
        "user": request.user,
        "reviewAmount": len(reviews),
        "reviewScore": sum(review.rating for review in reviews)
        / len(reviews)
        if len(reviews) > 0
        else 0,
    }
    return render(
        request=request,
        template_name="products/details.html",
        context=context,
    )
