from task_manager.users.models import User
from django.urls import reverse_lazy as reverse
from django.test import TestCase
from task_manager.tasks.models import Status, Task


class Create(TestCase):
    fixtures = ['db_task.json']

    def test_create_open_without_login(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_task(self):
        user = User.objects.first()
        self.client.force_login(user=user)
        status = Status.objects.first()

        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)

        task_count_before = Task.objects.count()

        response = self.client.post(
            reverse('task_create'),
            {
                'name': 'test task',
                'status': status.id,
                'executor': user.id,
                'description': 'test description'
                }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), task_count_before + 1)

        new_task = Task.objects.last()
        self.assertEqual(new_task.name, 'test task')
        self.assertEqual(new_task.status, status)
        self.assertEqual(new_task.author, user)
