from django.shortcuts import render, redirect, get_object_or_404
from main.models import Bouquet
from django.contrib.auth.decorators import login_required

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    bouquets = []
    total = 0
    for bouquet_id, quantity in cart.items():
        bouquet = get_object_or_404(Bouquet, id=bouquet_id)
        bouquet.quantity = quantity
        bouquet.total_price = bouquet.price * quantity
        bouquets.append(bouquet)
        total += bouquet.total_price
    return render(request, 'cart/cart.html', {'bouquets': bouquets, 'total': total})

@login_required
def add_to_cart(request, bouquet_id):
    cart = request.session.get('cart', {})
    cart[str(bouquet_id)] = cart.get(str(bouquet_id), 0) + 1
    request.session['cart'] = cart
    return redirect('main:catalog')

@login_required
def remove_from_cart(request, bouquet_id):
    cart = request.session.get('cart', {})
    if str(bouquet_id) in cart:
        del cart[str(bouquet_id)]
    request.session['cart'] = cart
    return redirect('cart:cart_view')


# Create your views here.
