import json
from django.urls import reverse_lazy as reverse
from django.test import TestCase
import os
from task_manager.users.models import User


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../fixtures'
)


class CreateTest(TestCase):

    def test_open_create_page(self):
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_redirect_user(self):
        fixture_file = os.path.join(FIXTURE_DIR, 'user.json')
        with open(fixture_file) as f:
            testuser = json.load(f)
        response = self.client.post(
            reverse('user_create'),
            testuser
        )
        self.assertRedirects(response, reverse('login'))
        user = User.objects.get(username=testuser.get('username'))
        self.assertEqual(user.username, testuser.get('username'))
        self.assertTrue(user.check_password(testuser.get('password1')))
