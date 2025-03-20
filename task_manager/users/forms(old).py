from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя',
            'required': True,
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Фамилия",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия',
            'required': True,
        })
    )

    username = forms.CharField(
        max_length=150,
        required=True,
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'required': True,
        }),
        help_text="Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_."  # noqa: E501
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'required': True,
        }),
        help_text="Ваш пароль должен содержать как минимум 3 символа."
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
            'required': True,
        }),
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
            )


def clean_username(self):
    username = self.cleaned_data.get('username')
    if User.objects.filter(username=username).exclude(id=self.instance.id).exists():  # noqa: E501
        raise forms.ValidationError('Пользователь с таким именем уже существует.')  # noqa: E501
    return username
