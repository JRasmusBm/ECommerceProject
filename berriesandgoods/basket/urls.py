from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("remove/<int:product_id>", views.removeProduct),
    path("change/<int:product_id>", views.changeAmount),
    path("checkout/", views.checkout)
]