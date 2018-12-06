from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("remove/<int:idproduct>", views.removeProduct),
    path("change/<int:idproduct>", views.changeAmount),
    path("checkout/", views.checkout)
]
