from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy


class MessageMixin:
    """Mixin for adding bootstrap-styled messages."""

    bootstrap_tags = {
        messages.SUCCESS: 'success',
        messages.ERROR: 'danger',
        messages.INFO: 'info',
        messages.WARNING: 'warning',
    }

    def add_message(self, request, level, message):
        tag = self.bootstrap_tags.get(level, '')
        messages.add_message(request, level, message, extra_tags=tag)

    def success(self, request, message):
        self.add_message(request, messages.SUCCESS, message)

    def error(self, request, message):
        self.add_message(request, messages.ERROR, message)

    def info(self, request, message):
        self.add_message(request, messages.INFO, message)

    def warning(self, request, message):
        self.add_message(request, messages.WARNING, message)


class AuthRequiredMixin(LoginRequiredMixin, MessageMixin):
    auth_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.error(request, self.auth_message)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(UserPassesTestMixin, MessageMixin):
    permission_message = None
    permission_url = None

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        self.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class DeleteProtectionMixin(MessageMixin):
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            self.error(request, self.protected_message)
            return redirect(self.protected_url)


class AuthorDeletionMixin(UserPassesTestMixin, MessageMixin):
    author_message = None
    author_url = None

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        self.error(self.request, self.author_message)
        return redirect(self.author_url)
