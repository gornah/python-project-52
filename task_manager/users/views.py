from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.mixins import (
    AuthRequiredMixin,
    UserPermissionMixin,
    DeleteProtectionMixin
)
from .models import User
from .forms import UserForm


class UsersListView(ListView):

    template_name = 'users/list.html'
    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):

    template_name = 'login.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(AuthRequiredMixin, UserPermissionMixin,
                     SuccessMessageMixin, UpdateView):

    template_name = 'login.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно изменен'
    permission_message = 'У вас нет прав для изменения другого пользователя.'
    permission_url = reverse_lazy('users')


class UserDeleteView(AuthRequiredMixin, UserPermissionMixin,
                     DeleteProtectionMixin, SuccessMessageMixin, DeleteView):

    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно удален'
    permission_message = 'У вас нет прав для изменения другого пользователя.'
    permission_url = reverse_lazy('users')
    protected_message = 'Невозможно удалить пользователя.'
    protected_url = reverse_lazy('users')
