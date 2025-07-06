from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .bot_integration import send_order_to_telegram

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        send_order_to_telegram(instance)
