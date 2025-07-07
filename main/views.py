from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bouquet, CartItem, Order
from .forms import OrderForm
from django.utils import timezone


def home(request):
    return render(request, 'main/home.html')


def catalog(request):
    bouquets = Bouquet.objects.all()
    return render(request, 'main/catalog.html', {'bouquets': bouquets})


@login_required
def add_to_cart(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, bouquet=bouquet)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'"{bouquet.name}" добавлен в корзину.')
    return redirect('main:catalog')


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.bouquet.price * item.quantity for item in cart_items)
    return render(request, 'main/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, 'Товар удалён из корзины.')
    return redirect('main:cart')



# 🔧 ДОБАВЛЕНО ДЛЯ УСТРАНЕНИЯ ОШИБКИ
@login_required
def cart_view(request):
    return view_cart(request)


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, 'Ваша корзина пуста.')
        return redirect('main:catalog')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            for item in cart_items:
                Order.objects.create(
                    user=request.user,
                    bouquet=item.bouquet,
                    delivery_address=form.cleaned_data['delivery_address'],
                    delivery_datetime=form.cleaned_data['delivery_datetime'],
                    comment=form.cleaned_data['comment'] or ''
                )
            cart_items.delete()
            messages.success(request, 'Ваш заказ успешно оформлен.')
            return redirect('main:catalog')
    else:
        form = OrderForm()
    return render(request, 'main/checkout.html', {'form': form})

