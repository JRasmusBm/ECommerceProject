from django.shortcuts import render, redirect
from django.db import connection
# from collections import namedtuple

from django.core.validators import MaxValueValidator, MinValueValidator

from home.models import Product, Review, Users
from .forms import AddToCartForm, EditReviewForm, SearchForm
from basket.orders import ordersBackend


def unpack_product(product):
    reviews = Review.objects.raw(
        "SELECT * FROM review WHERE idproduct=%s;", [product.idproduct]
    )
    return {
        "name": product.nameproduct,
        "availability": product.availability,
        "price": format(product.priceproduct / 100, ".2f"),
        "unit": product.nameproducttype.unit,
        "idproduct": product.idproduct,
        "image": product.img,
        "reviews": reviews,
        "reviewAmount": len(reviews),
        "reviewScore": sum(review.rating for review in reviews)
        / len(reviews)
        if len(reviews) > 0
        else 0,
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


# SELECT p
# FROM product as p
# INNER JOIN (SELECT idproduct, avg(rating) as rating
#         FROM review
#         GROUP BY idproduct) as r ON r.idproduct = p.idproduct
# ORDER BY rating DESC


# def namedtuplefetchall(query):
#     "Return all rows from a cursor as a namedtuple"
#     with connection.cursor() as cursor:
#         cursor.execute(*query)
#         columns = [col[0] for col in cursor.description]
#         nt_result = namedtuple("product", columns)
#         return [nt_result(*row) for row in cursor.fetchall()]


def build_query(flags):
    """Builds a query from the given flags.
    Return a tuple containing the string and the variables"""
    query_string = """SELECT p.idproduct, p.nameproduct, p.priceproduct, p.img,
    p.nameproduct, p.availability FROM product as p """
    if flags["reviews"] in ["highest", "lowest"]:
        query_string += """
        INNER JOIN (SELECT idproduct, avg(rating) as rating
                    FROM review
                    GROUP BY idproduct) as r ON r.idproduct = p.idproduct
        ORDER BY rating
        """
        if flags["reviews"] == "highest":
            query_string += " DESC"
    elif flags["price"] in ["highest", "lowest"]:
        query_string += " ORDER BY p.priceproduct"
        if flags["price"] == "highest":
            query_string += " DESC"
    elif flags["quantity"] in ["highest", "lowest"]:
        query_string += " ORDER BY p.availability"
        if flags["quantity"] == "highest":
            query_string += " DESC"
    else:
        query_string += " ORDER BY p.nameproduct"
    query_variables = []
    return (" ".join(query_string.split()), query_variables)


def index(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            return redirect("products:search", term=request.POST["search"])
    flags = {
        "reviews": request.GET.get("reviews", ""),
        "quantity": request.GET.get("quantity", ""),
        "price": request.GET.get("price", ""),
    }
    search_form = SearchForm()
    query = build_query(flags)
    products = Product.objects.raw(*query)
    context = {
        "search_form": search_form,
        "page_title": "Berries",
        "products": [unpack_product(product) for product in products],
        "user": request.user,
        "flags": flags,
        "query": query[0]
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
    context = {
        "page_title": "Reviews",
        "product": unpack_product(
            Product.objects.raw(
                "SELECT * FROM product WHERE idproduct=%s;", [idproduct]
            )[0]
        ),
    }
    return render(
        request=request,
        template_name="products/reviews.html",
        context=context,
    )


def details(request, idproduct, message="", success=""):
    product = Product.objects.raw(
        "SELECT * FROM product WHERE idproduct=%s;", [idproduct]
    )[0]
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login:login")
        form = AddToCartForm(request.POST)
        form.fields["amount"].validators = [
            MaxValueValidator(
                limit_value=product.availability,
                message="Not enough in stock",
            ),
            MinValueValidator(
                limit_value=1, message="Must be greater than 0"
            ),
        ]
        if form.is_valid():
            ordersBackend.addProduct(
                user=request.user,
                idproduct=idproduct,
                amount=int(form.data["amount"]),
            )
            return redirect(
                "products:details",
                idproduct=idproduct,
                message=" ".join(
                    f"""{form.data['amount']} {product.nameproducttype.unit} of
                    {product.nameproduct} added to shopping basket.""".split()
                ),
                success="true",
            )
        return redirect(
            "products:details",
            idproduct=idproduct,
            message=form.errors["amount"][0],
        )
    else:
        form = AddToCartForm()
    context = {
        "page_title": "Details",
        "product": unpack_product(
            Product.objects.raw(
                "SELECT * FROM product WHERE idproduct=%s;", [idproduct]
            )[0]
        ),
        "form": form,
        "success": success,
        "message": message,
        "user": request.user,
    }
    return render(
        request=request,
        template_name="products/details.html",
        context=context,
    )
