from django import forms
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from .models import User


class UserForm(forms.ModelForm):

    pass_min_len = 3

    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Имя",
        label_suffix='',
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
        label_suffix='',
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
        label_suffix='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'required': True,
        }),
        help_text="Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_."  # noqa: E501
    )

    password1 = forms.CharField(
        validators=[
            MinLengthValidator(pass_min_len, "Пароль слишком короткий"),
        ],
        label="Пароль",
        label_suffix='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'required': True,
        }),
        help_text="Ваш пароль должен содержать как минимум 3 символа."
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        label_suffix='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
            'required': True,
        }),
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз."
    )

    class Meta:
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

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get('password1')
        if password:
            user.password = make_password(password)

        if commit:
            user.save()

        return user
