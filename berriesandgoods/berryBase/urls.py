from django.urls import path
from . import views

urlpatterns = [
    path("details/<int:product_id>", views.details, name="details"),
    path("", views.index, name="index"),
]
