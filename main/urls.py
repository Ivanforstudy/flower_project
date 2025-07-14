from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:bouquet_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('buy/<int:bouquet_id>/', views.buy_now, name='buy_now'),
    path('success/', views.order_success, name='order_success'),
]
