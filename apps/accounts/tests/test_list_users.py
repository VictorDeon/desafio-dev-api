from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User


class ListUsersTestCase(APITestCase):
    """
    Testes unitários para verificar o comportamento
    de listagem de usuários.
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

        self.url = reverse('user-list')

    def tearDown(self):
        """
        Executado após cada teste.
        """

        User.objects.all().delete()
        self.client.logout()

    def test_list_all_users(self):
        """
        Lista todos os usuários do sistema.
        """

        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(User.objects.count(), 3)

    def test_list_all_not_deleted_users(self):
        """
        Lista todos os usuários que não foram deletados do sistema.
        """

        self.client.force_authenticate(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 3)

    def test_list_all_deleted_users(self):
        """
        Lista todos os usuários que foram deletados do sistema.
        """

        self.client.force_authenticate(self.superuser)
        response = self.client.get(f"{self.url}?deleted=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_user_by_email(self):
        """
        Lista todos os usuários pelo email.
        """

        self.client.force_authenticate(self.superuser)
        response = self.client.get(f"{self.url}?email=fulano02@gmail.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_not_filter_user_deleted(self):
        """
        Não pode filtrar usuário que já foram deletados
        """

        self.client.force_authenticate(self.superuser)
        response = self.client.get(f"{self.url}?email=fulano03@gmail.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_not_logged_user_list_users(self):
        """
        Usuário não autenticado não pode listar usuários.
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), "Usuário não tem autorização para realizar essa ação!")

    def test_not_admin_user_list_users(self):
        """
        Usuário que não são admin não pode listar usuários.
        """

        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), "Usuário não tem autorização para realizar essa ação!")
