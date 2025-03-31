from task_manager.users.models import User
from django.urls import reverse_lazy as reverse
from django.test import TransactionTestCase
from task_manager.tasks.models import Status, Task


class UpdateTask(TransactionTestCase):
    fixtures = ['db_task.json']

    def test_update_open_without_login(self):

        response = self.client.get(reverse('task_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('task_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_update_task(self):

        user = User.objects.first()
        self.client.force_login(user=user)

        response = self.client.get(reverse('task_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        task = Task.objects.first()
        status = Status.objects.first()
        user2 = User.objects.create_user(username='test', password='testpass')

        updated_task_data = {
            'name': 'test_task',
            'status': status.id,
            'executor': user2.id,
            'description': 'new description'
        }

        response = self.client.post(
            reverse('task_update', kwargs={'pk': task.id}),
            updated_task_data
        )

        self.assertEqual(response.status_code, 302)

        task.refresh_from_db()
        self.assertEqual(task.name, updated_task_data['name'])
        self.assertEqual(task.executor, user2)
        self.assertEqual(task.status, status)
        self.assertEqual(task.author, user)
