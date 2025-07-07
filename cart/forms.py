from django import forms

class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(label="Адрес доставки", max_length=255)
    delivery_datetime = forms.DateTimeField(label="Дата и время доставки", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    comment = forms.CharField(label="Комментарий", required=False, widget=forms.Textarea)
