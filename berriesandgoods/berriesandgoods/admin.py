from django.contrib import admin

# from login_manager.forms import LoginForm


class MyAdminSite(admin.AdminSite):
    site_title = "Berries and Goods | Admin"
    site_header = "Berries and Goods - Administration"
    index_title = "CustomLogin"
