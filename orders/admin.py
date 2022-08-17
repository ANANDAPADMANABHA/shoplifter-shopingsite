from django.contrib import admin
from. models import *
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ("product","quantity","price")
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ["user","orderid","ordertotal","payment",]
    list_filter = ["status","is_ordered"]
    search_fields = ["orderid","user"]
    list_per_page = 20
    inlines = [OrderProductInline]
    


admin.site.register(Orders,OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)
