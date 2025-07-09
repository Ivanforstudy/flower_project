from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].help_text = 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_'
        self.fields['email'].label = 'Электронная почта'
        self.fields['email'].help_text = 'Введите действующий адрес электронной почты'
        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].help_text = 'Пароль должен содержать минимум 8 символов, не быть слишком простым и отличаться от имени пользователя.'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password2'].help_text = 'Введите пароль ещё раз для подтверждения'

        self.error_messages = {
            'password_mismatch': 'Введённые пароли не совпадают.',
        }

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким адресом электронной почты уже зарегистрирован.')
        return email
