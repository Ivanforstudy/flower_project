from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('add_to_cart/<int:bouquet_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart_view'),
    path('remove_from_cart/<int:bouquet_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]