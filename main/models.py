# main/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Bouquet(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    image = models.ImageField("Изображение", upload_to='bouquet_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.bouquet.name} (x{self.quantity})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bouquets = models.ManyToManyField(Bouquet)
    delivery_address = models.CharField("Адрес доставки", max_length=255)
    delivery_datetime = models.DateTimeField("Дата и время доставки")
    comment = models.TextField("Комментарий", blank=True)
    total_price = models.DecimalField("Итоговая цена", max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.pk} от {self.user.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
