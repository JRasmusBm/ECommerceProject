from django.contrib import admin
from .models import Berry, Berrytype, Goods, Goodstype, Orders, Users

admin.site.register(Berry)
admin.site.register(Berrytype)
admin.site.register(Goods)
admin.site.register(Goodstype)
admin.site.register(Orders)
admin.site.register(Users)
