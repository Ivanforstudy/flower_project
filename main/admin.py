from django.contrib import admin
from .models import Bouquet, CartItem, Order, OrderItem


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    verbose_name = "Букет"
    verbose_name_plural = "Букеты"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'bouquet', 'quantity')
    list_filter = ('user', 'bouquet')
    verbose_name = "Товар в корзине"
    verbose_name_plural = "Товары в корзине"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'delivery_address', 'delivery_datetime', 'total_price')
    list_filter = ('delivery_datetime',)
    search_fields = ('user__email', 'delivery_address')
    inlines = [OrderItemInline]
    verbose_name = "Заказ"
    verbose_name_plural = "Заказы"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'bouquet', 'quantity')
    list_filter = ('order', 'bouquet')
    verbose_name = "Позиция заказа"
    verbose_name_plural = "Позиции заказа"
