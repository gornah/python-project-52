from task_manager.users.models import User
from django.urls import reverse_lazy as reverse
from django.test import TestCase
from task_manager.labels.models import Label


class CreateLabel(TestCase):
    fixtures = ['db_label.json']

    def test_create_open_without_login(self):
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_label(self):
        user = User.objects.first()
        self.client.force_login(user=user)

        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 200)

        label_count_before = Label.objects.count()

        response = self.client.post(reverse('label_create'), {'name': 'test'})

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Label.objects.count(), label_count_before + 1)

        new_label = Label.objects.last()
        self.assertEqual(new_label.name, 'test')
