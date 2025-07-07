from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Bouquet(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='bouquets/', verbose_name="Изображение")

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE, verbose_name="Букет")
    delivery_address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    delivery_datetime = models.DateTimeField(verbose_name="Дата и время доставки")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    order_datetime = models.DateTimeField(default=timezone.now, verbose_name="Дата оформления заказа")

    def __str__(self):
        return f"Заказ #{self.pk} от {self.user.username}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.bouquet.price

    def __str__(self):
        return f"{self.quantity} x {self.bouquet.name} ({self.user.username})"
