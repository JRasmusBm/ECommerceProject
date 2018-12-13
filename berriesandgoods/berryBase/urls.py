from django.urls import path
from . import views

urlpatterns = [
    path("details/<int:idproduct>", views.details, name="details"),
    path("details/<int:idproduct>/reviews", views.reviews, name="reviews"),
    path(
        "details/<int:idproduct>/reviews/edit",
        views.edit_reviews,
        name="edit_reviews",
    ),
    path(
        "details/<int:idproduct>/<message>", views.details, name="details"
    ),
    path(
        "details/<int:idproduct>/<message>/<success>",
        views.details,
        name="details",
    ),
    path("search/<term>", views.search, name="search"),
    path("", views.index, name="index"),
]
