from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User


class EditUserTestCase(APITestCase):
    """
    Testes unitários para verificar o comportamento
    de atualização de usuários.
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

    def test_update_own_data_by_admin(self):
        """
        O administrador atualizando seus próprios dados.
        """

        url = reverse('user-detail', kwargs={'pk': self.superuser.pk})

        data = {
            "name": 'Fulano Admin autalizado',
            "email": 'fulano-admin-updated@gmail.com',
            "deleted": True
        }

        self.client.force_authenticate(self.superuser)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.superuser.refresh_from_db()
        self.assertEqual(self.superuser.name, data['name'])
        self.assertEqual(self.superuser.email, data['email'])
        self.assertEqual(self.superuser.deleted, data['deleted'])

    def test_update_own_data_by_normal_user(self):
        """
        Usuário normal atualizando seus próprios dados.
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.pk})

        data = {
            "name": 'Fulano autalizado',
            "email": 'fulano-updated@gmail.com',
            "deleted": True
        }

        self.client.force_authenticate(self.user1)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.name, data['name'])
        self.assertEqual(self.user1.email, data['email'])
        self.assertEqual(self.user1.deleted, data['deleted'])

    def test_admin_update_normal_user_data(self):
        """
        Administrador pode atualizar os dados de um usuário normal.
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.pk})

        data = {
            "name": 'Fulano atualizado',
            "email": 'fulano-updated@gmail.com',
            "deleted": True
        }

        self.client.force_authenticate(self.superuser)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.name, data['name'])
        self.assertEqual(self.user1.email, data['email'])
        self.assertEqual(self.user1.deleted, data['deleted'])

    def test_not_normal_user_update_another_normal_user_data(self):
        """
        Usuário normal não pode atualizar os dados de outro usuário.
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.pk})

        data = {
            "name": 'Fulano atualizado',
            "email": 'fulano-updated@gmail.com',
            "deleted": True
        }

        self.client.force_authenticate(self.user2)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), "Usuário não tem autorização para realizar essa ação!")
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.name, "Fulano 01")
        self.assertEqual(self.user1.email, "fulano01@gmail.com")
        self.assertEqual(self.user1.deleted, False)

    def test_not_update_empty_name(self):
        """
        Não pode atualizar nome vazio.
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.pk})

        data = {
            "name": '',
            "email": 'fulano-updated@gmail.com',
            "deleted": True
        }

        self.client.force_authenticate(self.user1)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), "O nome do usuário não pode está vazio.")
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.name, "Fulano 01")

    def test_not_update_empty_email(self):
        """
        Não pode atualizar email vazio.
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.pk})

        data = {
            "name": 'Fulano atualizado',
            "email": '',
            "deleted": True
        }

        self.client.force_authenticate(self.user1)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), "O email do usuário não pode está vazio.")
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.email, "fulano01@gmail.com")

    def test_not_update_email_from_another_user(self):
        """
        Não pode atualizar email que já existe.
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.pk})

        data = {
            "name": 'Fulano atualizado',
            "email": 'fulano03@gmail.com',
            "deleted": True
        }

        self.client.force_authenticate(self.user1)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), "Já existe um usuário com esse email")
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.email, "fulano01@gmail.com")

    def test_update_few_fields(self):
        """
        Testando a atualização de apenas alguns dados.
        """

        url = reverse('user-detail', kwargs={'pk': self.user1.pk})

        data = {
            "name": 'Fulano atualizado',
            "email": 'fulano-updated@gmail.com',
        }

        self.client.force_authenticate(self.user1)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.name, data['name'])
        self.assertEqual(self.user1.email, data['email'])
        self.assertEqual(self.user1.deleted, False)
