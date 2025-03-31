from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.mixins import (
    AuthRequiredMixin,
    UserPermissionMixin,
    DeleteProtectionMixin,
    MessageMixin
)
from .models import User
from .forms import UserForm


class UsersListView(ListView):
    '''
    Show all Users
    '''
    template_name = 'users/list.html'
    model = User
    context_object_name = 'users'


class UserCreateView(MessageMixin, CreateView):
    '''
    Create new User
    '''
    template_name = 'users/create.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    extra_context = {
        'header': 'Регистрация',
        'button_title': 'Зарегистрировать',
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success(self.request, 'Пользователь успешно зарегистрирован')
        return response


class UserUpdateView(AuthRequiredMixin, UserPermissionMixin,
                     MessageMixin, UpdateView):
    '''
    Edit existing User. User authorization is required
    User can only edit himself
    '''
    template_name = 'users/create.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users')
    extra_context = {
        'header': 'Изменение пользователя',
        'button_title': 'Изменить',
    }
    permission_message = 'У вас нет прав для изменения другого пользователя.'
    permission_url = reverse_lazy('users')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success(self.request, 'Пользователь успешно изменен')
        return response

    def handle_no_permission(self):
        self.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class UserDeleteView(AuthRequiredMixin, UserPermissionMixin,
                     DeleteProtectionMixin, SuccessMessageMixin, DeleteView):
    '''
    Delete existing User. User authorization is required
    User can only delete himself
    User cannot be deleted if associated with a task
    '''
    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно удален'
    permission_message = 'У вас нет прав для изменения другого пользователя.'
    permission_url = reverse_lazy('users')
    protected_message = 'Невозможно удалить пользователя.'
    protected_url = reverse_lazy('users')
