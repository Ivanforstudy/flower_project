from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)


class OrderForm(forms.ModelForm):
    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    delivery_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Order
        fields = ['flower', 'address', 'delivery_date', 'delivery_time', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
