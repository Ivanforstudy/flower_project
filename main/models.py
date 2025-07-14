# файл: main/models.py

from django.db import models
from django.conf import settings


class Bouquet(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    image = models.ImageField("Изображение", upload_to='bouquet_images/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    bouquet = models.ForeignKey(
        Bouquet,
        on_delete=models.CASCADE,
        verbose_name="Букет"
    )
    quantity = models.PositiveIntegerField("Количество", default=1)

    def __str__(self):
        return f"{self.quantity} x {self.bouquet.name}"

    class Meta:
        verbose_name = "Позиция в корзине"
        verbose_name_plural = "Корзина"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    delivery_address = models.CharField("Адрес доставки", max_length=255)
    delivery_datetime = models.DateTimeField("Дата и время доставки")
    comment = models.TextField("Комментарий", blank=True, null=True)
    total_price = models.DecimalField("Общая сумма", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.pk} от {self.user.email}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Заказ"
    )
    bouquet = models.ForeignKey(
        Bouquet,
        on_delete=models.CASCADE,
        verbose_name="Букет"
    )
    quantity = models.PositiveIntegerField("Количество", default=1)

    def __str__(self):
        return f"{self.quantity} x {self.bouquet.name} (заказ #{self.order.pk})"

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"
