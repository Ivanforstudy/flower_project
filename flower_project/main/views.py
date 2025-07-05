
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, OrderForm
from .models import Flower, Order


def home(request):
    return render(request, 'main/home.html')


def catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'main/catalog.html', {'flowers': flowers})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'main/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def order_view(request, flower_id):
    flower = Flower.objects.get(pk=flower_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.flower = flower
            order.save()
            return redirect('my_orders')
    else:
        form = OrderForm()
    return render(request, 'main/order.html', {'form': form, 'flower': flower})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/my_orders.html', {'orders': orders})