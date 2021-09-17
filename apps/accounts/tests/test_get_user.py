from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User


class GetUserTestCase(APITestCase):
    """
    Testes unitários para verificar o comportamento
    de pegar os dados de um usuário.
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

        User.objects.all().delete()
        self.client.logout()

    def test_get_you_own_data_by_admin_user(self):
        """
        Pega seus próprios dados como admin.
        """

        url = reverse('user-detail', kwargs={'pk': self.superuser.pk})
        self.client.force_authenticate(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), self.superuser.email)

    def test_get_another_user_data_from_admin(self):
        """
        Pega dados de outros usuário por um administrador.
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.pk})
        self.client.force_authenticate(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), self.user1.email)

    def test_get_own_data_from_normal_user(self):
        """
        Pega seus próprios dados como usuário normal.
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.pk})
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), self.user1.email)

    def test_get_own_data_from_logged_user(self):
        """
        Pega seus próprios dados como usuário normal.
        """

        url = reverse('user-current-user')
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), self.user1.email)

    def test_not_get_data_from_normal_user_by_normal_user(self):
        """
        Usuário normal não poder pegar dados de outro usuário normal.
        """

        url = reverse('user-detail', kwargs={'pk': self.user2.pk})
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), "Usuário não tem autorização para realizar essa ação!")

    def test_not_logged_user_can_get_own_data(self):
        """
        Usuário não autenticado não pode pegar seus dados.
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), "Usuário não autenticado!")

    def test_get_deleted_user_data_by_admin(self):
        """
        Pega os dados de um usuário deletado.
        """

        url = reverse('user-detail', kwargs={'pk': self.user3.pk})
        self.client.force_authenticate(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
