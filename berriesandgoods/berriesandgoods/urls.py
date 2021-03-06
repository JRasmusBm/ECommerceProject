"""berriesandgoods URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from login_manager import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "login/",
        include(("login_manager.urls", "login"), namespace="login"),
    ),
    path("logout/", views.log_out, name="logout"),
    path("", include(("home.urls", "home"), namespace="home")),
    path("about/", include(("about.urls", "about"), namespace="about")),
    path(
        "products/",
        include(("berryBase.urls", "products"), namespace="products"),
    ),
    path("filter/", include(("filter.urls", "filter"), namespace="filter")),
    path(
        "basket/",
        include(("basket.urls", "basket"), namespace="basket"),
    ),
    path(
        "view_orders/",
        include(("view_orders.urls", "view_orders"), namespace="view_orders"),
    ),
]
