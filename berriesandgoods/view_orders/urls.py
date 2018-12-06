from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("remove/<int:idorders>", views.removeOrder),
    path("admin/", views.admin, name="admin"),
    path("admin/remove/<int:idorders>", views.removeOrderAdmin),
    path("admin/handle/<int:idorders>", views.handleOrder),
]
