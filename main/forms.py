from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    delivery_address = forms.CharField(label='Адрес доставки', widget=forms.TextInput(attrs={'class': 'form-control'}))
    delivery_datetime = forms.DateTimeField(
        label='Дата и время доставки',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M')
    )
    comment = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = Order
        fields = ['delivery_address', 'delivery_datetime', 'comment']