from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'delivery_datetime', 'comment']
        widgets = {
            'delivery_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'delivery_address': 'Адрес доставки',
            'delivery_datetime': 'Дата и время доставки',
            'comment': 'Комментарий к заказу',
        }
