from django.contrib import admin
from .models import Flower, Order

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'flower', 'delivery_date', 'delivery_time', 'created_at')
    list_filter = ('delivery_date',)
    search_fields = ('user__username', 'address')
