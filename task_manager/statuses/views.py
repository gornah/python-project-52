from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from .models import Status
from .forms import StatusForm


class StatusesListView(AuthRequiredMixin, ListView):
    '''
    Show all Statuses. User authorization is required
    '''
    template_name = 'statuses/list.html'
    model = Status
    context_object_name = 'statuses'
    extra_context = {
        'header': 'Статусы'
    }


class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    '''
    Create new Status. User authorization is required
    '''
    template_name = 'statuses/create.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = 'Статус успешно создан'
    extra_context = {
        'header': 'Создать статус',
        'button_title': 'Создать',
    }


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    '''
    Edit existing Status. User authorization is required
    '''
    template_name = 'statuses/create.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = 'Статус успешно изменен'
    extra_context = {
        'header': 'Изменение статуса',
        'button_title': 'Изменить',
    }


class StatusDeleteView(AuthRequiredMixin, DeleteProtectionMixin,
                       SuccessMessageMixin, DeleteView):
    '''
    Delete existing Status. User authorization is required
    If the status is associated with at least one task it cannot be deleted.
    '''
    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = 'Статус успешно удален'
    protected_message = 'Невозможно удалить статус, он используется'
    protected_url = reverse_lazy('statuses')
    extra_context = {
        'header': 'Удаление статуса',
        'button_title': 'Да, удалить',
    }
