from task_manager.users.models import User
from django.urls import reverse_lazy as reverse
from django.test import TestCase


class List(TestCase):
    fixtures = ['db_status.json']

    def test_open_create_without_login(self):
        response = self.client.get(reverse('statuses'))
        self.assertRedirects(response, reverse('login'))

    def test_list_with_login(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)

        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
