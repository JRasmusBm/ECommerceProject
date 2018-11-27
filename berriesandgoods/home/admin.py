from django.contrib import admin

from .models import Orderitems, Producttype, Product, Orders

admin.site.register(Orderitems)
admin.site.register(Producttype)
admin.site.register(Product)
admin.site.register(Orders)
