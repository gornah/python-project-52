from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=150, required=True, label="First name"
    )
    last_name = forms.CharField(
        max_length=150, required=True, label="Last name"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'password1', 'password2'
                  )
