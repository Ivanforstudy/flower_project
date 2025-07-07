from django.contrib import admin
from django.contrib.auth.models import User
from main.models import Bouquet, Order

admin.site.unregister(User)
admin.site.register(User)

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'bouquet', 'delivery_address', 'delivery_datetime', 'order_datetime')
    search_fields = ('user__username', 'bouquet__name', 'delivery_address')