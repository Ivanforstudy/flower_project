from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Bouquet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='bouquet_images/', blank=True, null=True)

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
        return f"{self.quantity} x {self.bouquet.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bouquets = models.ManyToManyField(Bouquet)
    delivery_address = models.CharField(max_length=255)
    delivery_datetime = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"
