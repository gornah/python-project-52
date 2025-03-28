from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
from django import forms

from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.labels.models import Label


class TaskFilter(FilterSet):

    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка',
        widget=forms.Select(
            attrs={
                'class': 'form-select ml-2 mr-3',
            }
        )
    )

    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
        widget=forms.Select(
            attrs={
                'class': 'form-select ml-2 mr-3',
            }
        )
    )

    executor = ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель',
        widget=forms.Select(
            attrs={
                'class': 'form-select ml-2 mr-3',
            }
        )
    )

    own_tasks = BooleanFilter(
        label='Только свои задачи',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input mr-3',
            }
        ),
        method='get_own_tasks',
    )

    def get_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'own_tasks']
