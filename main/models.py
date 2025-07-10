from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # <-- добавьте этот импорт
from django.conf import settings

from django.db import models
from django.conf import settings

class Bouquet(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='bouquet_images/', blank=True, null=True, verbose_name='Изображение')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bouquets = models.ManyToManyField(Bouquet, related_name='orders', verbose_name='Букеты')
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    delivery_datetime = models.DateTimeField(verbose_name='Дата и время доставки')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая стоимость')

    def __str__(self):
        return f'Заказ №{self.id} от {self.user}'

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.pk} от {self.user}"