from django import forms
from .models import Label


class LabelForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя",
        label_suffix='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя'
            }),
        )

    class Meta:
        model = Label
        fields = ['name']
