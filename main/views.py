from django.shortcuts import render, redirect, get_object_or_404
from .models import Bouquet, Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required

def home(request):
    bouquets = Bouquet.objects.all()
    return render(request, 'main/home.html', {'bouquets': bouquets})

@login_required
def create_order(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.bouquet = bouquet
            order.save()
            return redirect('home')  # можно на страницу "успешно"
    else:
        form = OrderForm()
    return render(request, 'main/create_order.html', {'form': form, 'bouquet': bouquet})

def catalog(request):
    bouquets = Bouquet.objects.all()
    return render(request, 'main/catalog.html', {'bouquets': bouquets})