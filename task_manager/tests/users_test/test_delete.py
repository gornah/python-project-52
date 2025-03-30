from django.urls import reverse_lazy as reverse
from django.test import TransactionTestCase
from task_manager.users.models import User


class Delete(TransactionTestCase):
    fixtures = ['db.json']

    def test_delete_without_login(self):
        response = self.client.post(
            reverse(
                'user_delete',
                kwargs={'pk': 1}
            )
        )
        self.assertRedirects(response, reverse('login'))
        users = User.objects.all().count()
        self.assertEqual(users, 1)

    def test_delete_only_himself(self):

        user1 = User.objects.first()

        user2 = User.objects.create_user(username='john', password='smith')

        self.client.login(username='john', password='smith')

        response = self.client.post(
            reverse(
                'user_delete',
                kwargs={'pk': user1.id}
            )
        )

        self.assertRedirects(response, reverse('users'))

        self.assertIn(user1, User.objects.all())
        self.assertEqual(User.objects.all().count(), 2)
        response = self.client.post(
            reverse(
                'user_delete',
                kwargs={'pk': user2.id}
            )
        )

        self.assertRedirects(response, reverse('users'))

        self.assertEqual(User.objects.all().count(), 1)
        self.assertNotIn(user2, User.objects.all())
