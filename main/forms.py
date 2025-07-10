from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    delivery_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        label='Дата и время доставки'
    )

    class Meta:
        model = Order
        fields = ['delivery_address', 'delivery_datetime', 'comment']
        labels = {
            'delivery_address': 'Адрес доставки',
            'comment': 'Комментарий к заказу',
        }
