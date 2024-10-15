from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

from django.contrib.auth import get_user_model

User = get_user_model()
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control mb-1", 'placeholder': 'Enter Username'}))
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Enter your E-Mail'}))
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={"class": "form-control mb-1", 'placeholder': 'Enter password'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={"class": "form-control mb-1", 'placeholder': 'Confirm Password'}))
    phone_number = forms.CharField(
        label="Мобильный телефон",
        max_length=12,  # Длина номера телефона, измените при необходимости
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter the phone number',  # Подсказка внутри поля ввода
                'class': 'form-control',  # CSS-класс для стилизации, если нужно
                'type': 'tel',  # HTML5 атрибут для типа ввода телефона
                'pattern': r'^\+?1?\d{11}$',  # Пример паттерна для проверки
            }
        )
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','phone_number']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Username'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(
                                   attrs={"class": "form-control mb-1", 'placeholder': 'Password'}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Username'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Username'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control mb-1", 'placeholder': 'Username'}))
    bio = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']




