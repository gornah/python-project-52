from task_manager.users.models import User
from django.urls import reverse_lazy as reverse
from django.test import TransactionTestCase
from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class DeleteLabelWithTask(TransactionTestCase):
    fixtures = ['db_bounded_label.json']

    def test_delete_label_with_task(self):
        label = Label.objects.first()
        user = User.objects.first()

        self.assertIsNotNone(label)
        self.assertIsNotNone(user)

        self.assertTrue(Task.objects.filter(labels=label).exists())

        self.client.force_login(user=user)

        response = self.client.post(
            reverse('label_delete', kwargs={'pk': label.id})
            )

        self.assertRedirects(response, reverse('labels'))

        self.assertEqual(Label.objects.count(), 1)
