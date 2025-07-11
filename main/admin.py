from django.contrib import admin
from .models import Bouquet, Order, OrderItem

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'delivery_address', 'delivery_date', 'delivery_time', 'total_price', 'get_bouquets')
    list_filter = ('delivery_date',)
    search_fields = ('user__email', 'delivery_address')
    inlines = [OrderItemInline]

    def get_bouquets(self, obj):
        return ", ".join([item.bouquet.name for item in obj.items.all()])
    get_bouquets.short_description = "Букеты"
