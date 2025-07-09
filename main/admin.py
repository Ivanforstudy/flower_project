from django.contrib import admin
from .models import Bouquet, Order

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'bouquet', 'delivery_address', 'delivery_datetime', 'created_at')

# Настройки панели администратора
admin.site.site_header = "Магазин букетов"
admin.site.index_title = "Администрирование"
admin.site.site_title = "Панель администратора"
