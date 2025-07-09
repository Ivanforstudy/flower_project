from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # <-- добавьте этот импорт

class Bouquet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='bouquets/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bouquet = models.ForeignKey('Bouquet', on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    delivery_datetime = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # timezone теперь определён

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.pk} от {self.user}"