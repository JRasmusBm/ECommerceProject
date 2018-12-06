from django.contrib import admin

from home.models import Orderitems, Producttype, Product, Orders, Review
from .forms import Users, UserAdmin


admin.site.register(Users, UserAdmin)
admin.site.register(Orderitems)
admin.site.register(Producttype)
admin.site.register(Product)
admin.site.register(Orders)
admin.site.register(Review)
