from django.urls import path
from . import views

urlpatterns = [
    path("create", views.new_user, name="create_user"),
    path("<message>", views.login_screen, name="login"),
    path("", views.login_screen, name="login"),
]
