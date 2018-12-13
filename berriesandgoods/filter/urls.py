from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.sort_by_price, name="filter"),
]
