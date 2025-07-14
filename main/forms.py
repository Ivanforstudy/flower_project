# файл: main/forms.py

from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    delivery_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Дата и время доставки"
    )

    class Meta:
        model = Order
        fields = ['delivery_address', 'delivery_datetime', 'comment']
        labels = {
            'delivery_address': 'Адрес доставки',
            'comment': 'Комментарий (необязательно)',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
