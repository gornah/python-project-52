from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from .mixins import MessageMixin


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(MessageMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success(self.request, 'Вы залогинены')
        return response

    def form_invalid(self, form):
        self.error(
            self.request,
            "Пожалуйста, введите корректные имя пользователя и пароль."
        )
        return super().form_invalid(form)


class UserLogoutView(MessageMixin, LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        self.info(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
