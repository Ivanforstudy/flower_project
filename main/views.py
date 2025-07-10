from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Bouquet, CartItem, Order
from .forms import OrderForm
from telegram_bot.bot import send_order_notification


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
    messages.success(request, f'Букет "{bouquet.name}" добавлен в корзину.')
    return redirect('main:cart_view')


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.bouquet.price * item.quantity for item in cart_items)
    return render(request, 'main/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request, bouquet_id):
    item = get_object_or_404(CartItem, user=request.user, bouquet_id=bouquet_id)
    item.delete()
    messages.info(request, 'Букет удалён из корзины.')
    return redirect('main:cart_view')


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
                order = Order.objects.create(
                    user=request.user,
                    delivery_address=form.cleaned_data['delivery_address'],
                    delivery_datetime=form.cleaned_data['delivery_datetime'],
                    comment=form.cleaned_data['comment'] or '',
                    total_price=item.bouquet.price * item.quantity
                )
                order.bouquets.add(item.bouquet)
                send_order_notification(item.bouquet, order)
            cart_items.delete()
            messages.success(request, 'Ваш заказ успешно оформлен.')
            return redirect('main:спасибо')
    else:
        form = OrderForm()

    return render(request, 'main/create_order.html', {'form': form})


@login_required
def buy_now(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = bouquet.price
            order.save()
            order.bouquets.add(bouquet)
            send_order_notification(bouquet, order)
            messages.success(request, f'Вы оформили заказ на букет: {bouquet.name}')
            return redirect('main:спасибо')
    else:
        form = OrderForm()

    return render(request, 'main/create_order.html', {
        'form': form,
        'single_bouquet': bouquet
    })


@login_required
def thank_you(request):
    return render(request, 'main/спасибо.html')
