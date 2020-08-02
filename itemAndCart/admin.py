from django.contrib import admin
from .models import Item,Order,OrderItem

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'discounted_price','seller')
    list_filter = ('category','price')
    search_fields = ('title','category')




admin.site.register(Item,ItemAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)