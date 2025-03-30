from task_manager.users.models import User
from django.urls import reverse_lazy as reverse
from django.test import TestCase
from task_manager.labels.models import Label


class UpdateLabel(TestCase):  # Исправил название класса
    fixtures = ['db_label.json']

    def test_update_open_without_login(self):
        response = self.client.get(reverse('label_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_update_label(self):
        user = User.objects.first()
        self.assertIsNotNone(user)
        self.client.force_login(user=user)

        label = Label.objects.filter(pk=1).first()
        self.assertIsNotNone(label)

        response = self.client.get(
            reverse('label_update', kwargs={'pk': label.pk})
            )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('label_update', kwargs={'pk': label.pk}),
            {'name': 'test'}
        )

        label.refresh_from_db()
        self.assertEqual(label.name, 'test')
