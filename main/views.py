from django.shortcuts import render, redirect, get_object_or_404
from .models import Bouquet, CartItem, Order, OrderItem
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required
from .telegram_utils import send_order_to_telegram


def index(request):
    popular_bouquets = Bouquet.objects.all()[:4]
    return render(request, 'main/home.html', {'popular_bouquets': popular_bouquets})


def catalog(request):
    bouquets = Bouquet.objects.all()
    return render(request, 'main/catalog.html', {'bouquets': bouquets})


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'main/cart.html', {'cart_items': cart_items})


@login_required
def add_to_cart(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, bouquet=bouquet)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('main:cart_view')


@login_required
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('main:cart_view')


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('main:cart_view')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            total_price = sum(item.bouquet.price * item.quantity for item in cart_items)
            order = Order.objects.create(
                user=request.user,
                delivery_address=form.cleaned_data['delivery_address'],
                delivery_datetime=form.cleaned_data['delivery_datetime'],
                comment=form.cleaned_data['comment'] or '',
                total_price=total_price
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    bouquet=item.bouquet,
                    quantity=item.quantity
                )
            cart_items.delete()
            send_order_to_telegram(order)
            return redirect('main:order_success')
    else:
        form = CheckoutForm()
    return render(request, 'main/checkout.html', {'form': form})


@login_required
def buy_now(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                delivery_address=form.cleaned_data['delivery_address'],
                delivery_datetime=form.cleaned_data['delivery_datetime'],
                comment=form.cleaned_data['comment'] or '',
                total_price=bouquet.price
            )
            OrderItem.objects.create(
                order=order,
                bouquet=bouquet,
                quantity=1
            )
            send_order_to_telegram(order)
            return redirect('main:order_success')
    else:
        form = CheckoutForm()
    return render(request, 'main/buy_now.html', {'form': form, 'bouquet': bouquet})


def order_success(request):
    return render(request, 'main/order_success.html')


