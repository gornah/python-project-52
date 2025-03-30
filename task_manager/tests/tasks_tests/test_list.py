from task_manager.users.models import User
from django.urls import reverse_lazy as reverse
from django.test import TransactionTestCase
from task_manager.tasks.models import Task


class List(TransactionTestCase):
    fixtures = ['db_task.json']

    def test_list_without_login(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)

    def test_list_with_login(self):
        user = User.objects.first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.all().count(), 1)
        task = Task.objects.first()
        task.delete()
        self.assertEqual(Task.objects.all().count(), 0)
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
