from django.contrib import admin
from .models import Item,Order,OrderItem

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'discounted_price','seller')
    list_filter = ('category','price')
    search_fields = ('title','category')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','ordered_date','amount','saving')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item','user','quantity','amount','saving')


admin.site.register(Item,ItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)