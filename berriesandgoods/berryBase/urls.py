from django.urls import path
from . import views

urlpatterns = [
    path('details/<int:item_id>', views.details, name="details"),
    path('', views.index, name="index"),
]
