from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User


class DeleteUserTestCase(APITestCase):
    """
    Testes unitários para verificar o comportamento
    de deleção de usuários.
    """

    def setUp(self):
        """
        Roda antes de cada método.
        """

        self.superuser = User.objects.create_superuser(
            name='Fulano Admin',
            email='fulano-admin@gmail.com',
            password='django1234'
        )

        self.user1 = User.objects.create_user(
            name='Fulano 01',
            email='fulano01@gmail.com',
            password='django1234'
        )

        self.user2 = User.objects.create_user(
            name='Fulano 02',
            email='fulano02@gmail.com',
            password='django1234'
        )

        self.user3 = User.objects.create_user(
            name='Fulano 03',
            email='fulano03@gmail.com',
            password='django1234'
        )
        self.user3.deleted = True
        self.user3.save()

    def tearDown(self):
        """
        Executado após cada teste.
        """

        User.raw_objects.all().delete()
        self.client.logout()

    def test_delete_own_superuser(self):
        """
        Administrador deletar sua própria conta.
        """

        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.raw_objects.count(), 4)
        url = reverse('user-detail', kwargs={'pk': self.superuser.pk})
        self.client.force_authenticate(self.superuser)
        response = self.client.delete(url)
        self.superuser.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.raw_objects.count(), 4)
        self.assertEqual(self.superuser.deleted, True)

    def test_delete_own_user(self):
        """
        Usuário comum deletando sua própria conta.
        """

        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.raw_objects.count(), 4)
        url = reverse('user-detail', kwargs={'pk': self.user1.pk})
        self.client.force_authenticate(self.user1)
        response = self.client.delete(url)
        self.user1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.raw_objects.count(), 4)
        self.assertEqual(self.user1.deleted, True)

    def test_delete_user_by_admin(self):
        """
        Administrador pode deletar a conta de um usuário.
        """

        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.raw_objects.count(), 4)
        url = reverse('user-detail', kwargs={'pk': self.user1.pk})
        self.client.force_authenticate(self.superuser)
        response = self.client.delete(url)
        self.user1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.raw_objects.count(), 4)
        self.assertEqual(self.user1.deleted, True)

    def test_not_delete_user_by_another_user(self):
        """
        Usuário normal não pode deletar outro usuário normal.
        """

        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.raw_objects.count(), 4)
        url = reverse('user-detail', kwargs={'pk': self.user1.pk})
        self.client.force_authenticate(self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.data.get('detail'), "Usuário não tem autorização para realizar essa ação!")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.user1.refresh_from_db()
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.raw_objects.count(), 4)
        self.assertEqual(self.user1.deleted, False)

    def test_not_delete_user_already_deleted(self):
        """
        Não pode deletar usuários que já foram deleados.
        """

        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.raw_objects.count(), 4)
        url = reverse('user-detail', kwargs={'pk': self.user3.pk})
        self.client.force_authenticate(self.superuser)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.user3.refresh_from_db()
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.raw_objects.count(), 4)
        self.assertEqual(self.user3.deleted, True)
