from django.contrib import admin
from .models import Bouquet, Order

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'delivery_address', 'delivery_datetime', 'total_price', 'get_bouquets')
    list_filter = ('delivery_datetime',)
    search_fields = ('user__username', 'delivery_address')

    def get_bouquets(self, obj):
        return ", ".join([b.name for b in obj.bouquets.all()])
    get_bouquets.short_description = "Букеты"
