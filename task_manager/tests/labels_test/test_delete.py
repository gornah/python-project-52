from task_manager.users.models import User
from django.urls import reverse_lazy as reverse
from django.test import TestCase
from task_manager.labels.models import Label


class DeleteLabel(TestCase):
    fixtures = ['db_label.json']

    def test_delete_open_without_login(self):
        response = self.client.get(reverse('label_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_delete_label(self):
        user = User.objects.first()
        self.client.force_login(user=user)

        response = self.client.get(reverse('label_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('label_delete', kwargs={'pk': 1}))
        self.assertEqual(Label.objects.count(), 0)
