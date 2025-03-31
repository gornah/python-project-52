from django import forms
from .models import Status


class StatusForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя",
        label_suffix='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя'
            }),
        )

    class Meta:
        model = Status
        fields = ['name']
