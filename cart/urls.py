from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('add/<int:bouquet_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:bouquet_id>/', views.remove_from_cart, name='remove_from_cart'),
]