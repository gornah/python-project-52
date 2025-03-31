from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView

from task_manager.mixins import AuthRequiredMixin, AuthorDeletionMixin
from task_manager.users.models import User
from .models import Task
from .forms import TaskForm
from .filters import TaskFilter


class TasksListView(AuthRequiredMixin, FilterView):
    '''
    Show all Tasks. User authorization is required
    '''
    template_name = 'tasks/list.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    extra_context = {
        'header': 'Задачи'
    }


class TaskDetailView(AuthRequiredMixin, DetailView):
    '''
    Show Task details. User authorization is required
    '''
    template_name = 'tasks/detail.html'
    model = Task
    context_object_name = 'task'
    extra_context = {
        'header': 'Task preview'
    }


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    '''
    Create new Task. User authorization is required
    '''
    template_name = 'tasks/create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно создана'
    extra_context = {
        'header': 'Создать задачу',
        'button_title': 'Создать',
    }

    def form_valid(self, form):

        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    '''
    Edit existing Task. User authorization is required
    '''
    template_name = 'tasks/create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно изменена'
    extra_context = {
        'header': 'Изменение задачи',
        'button_title': 'Изменить',
    }


class TaskDeleteView(AuthRequiredMixin, AuthorDeletionMixin,
                     SuccessMessageMixin, DeleteView):
    '''
    Delete existing Task. User authorization is required
    Only the author can delete his tasks.
    '''
    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно удалена'
    author_message = 'Задачу может удалить только ее автор'
    author_url = reverse_lazy('tasks')
    extra_context = {
        'header': 'Удаление задачи',
        'button_title': 'Да, удалить',
    }
