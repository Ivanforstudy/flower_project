from django.db import models
from django.conf import settings


# Один букет (товар)
class Bouquet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='bouquets/')

    def __str__(self):
        return self.name


# Заказ
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    delivery_address = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Заказ #{self.pk} от {self.user.email}"


# Связь заказ — букет (позиции в заказе)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.bouquet.name}"


# Элемент корзины (до оформления заказа)
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.bouquet.name} ({self.user.email})"
