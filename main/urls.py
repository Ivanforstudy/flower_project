# main/urls.py
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('order/<int:bouquet_id>/', views.create_order, name='create_order'),
]