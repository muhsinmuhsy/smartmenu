from django.contrib import admin
from adminapp. models import *
# Register your models here.
admin.site.register(Category)

admin.site.register(Product)

admin.site.register(ProductPrice)

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product_price', 'quantity' ]
    
# admin.site.register(Order)
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_type', 'name', 'date', 'status' ]
    
admin.site.register(User)

admin.site.register(Table)

