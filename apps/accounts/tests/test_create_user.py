from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User


class CreateUserTestCase(APITestCase):
    """
    Testes unitários para verificar o comportamento
    de criação do usuário.
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

        self.user = User.objects.create_user(
            name='Fulano 01',
            email='fulano01@gmail.com',
            password='django1234'
        )

        self.data = {
            'name': 'Fulano 02',
            'email': 'fulano02@gmail.com',
            'password': 'django1234',
            'confirm_password': 'django1234'
        }

        self.url = reverse('user-list')

    def tearDown(self):
        """
        Executado após cada teste.
        """

        User.raw_objects.all().delete()
        self.client.logout()

    def test_create_user_by_superuser(self):
        """
        Cria um usuário pelo superusuário.
        """

        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_not_create_user_by_another_user(self):
        """
        Um usuário normal não pode criar outro usuário.
        """

        self.client.force_authenticate(self.user)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "Usuário não tem autorização para realizar essa ação!")

    def test_not_create_user_by_not_logged_user(self):
        """
        Só pode criar usuário com usuário autenticado.
        """

        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "Usuário não tem autorização para realizar essa ação!")

    def test_not_pass_name_in_payload(self):
        """
        Testando o caso que não foi passado o atributo name no payload.
        """

        del self.data['name']
        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "O nome do usuário é obrigatório.")

    def test_empty_name_in_payload(self):
        """
        Testando o caso que foi passado um name vazio.
        """

        self.data['name'] = ""
        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "O nome do usuário não pode está vazio.")

    def test_not_pass_email_in_payload(self):
        """
        Testando o caso que não foi passado o atributo email no payload.
        """

        del self.data['email']
        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "O email do usuário é obrigatório.")

    def test_empty_email_in_payload(self):
        """
        Testando o caso que foi passado um email vazio.
        """

        self.data['email'] = ""
        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "O email do usuário não pode está vazio.")

    def test_invalid_email_in_payload(self):
        """
        Testando o caso que foi passado um email inválido.
        """

        self.data['email'] = "fulanogmail.com"
        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "O campo email não está no formato correto.")

    def test_not_pass_password_in_payload(self):
        """
        Testando o caso que não foi passado o atributo password no payload.
        """

        del self.data['password']
        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "A senha do usuário é obrigatório.")

    def test_empty_password_in_payload(self):
        """
        Testando o caso que foi passado um password vazio.
        """

        self.data['password'] = ""
        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "A senha do usuário não pode está vazio.")

    def test_not_pass_confirm_password_in_payload(self):
        """
        Testando o caso que não foi passado o atributo confirm_password no payload.
        """

        del self.data['confirm_password']
        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "A confirmação da senha do usuário é obrigatório.")

    def test_empty_confirm_password_in_payload(self):
        """
        Testando o caso que foi passado um confirm_password vazio.
        """

        self.data['confirm_password'] = ""
        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "A confirmação da senha do usuário não pode está vazio.")

    def test_confirm_password_not_match(self):
        """
        Testando o caso que as senhas não batem.
        """

        self.data['confirm_password'] = "django123"
        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "As senhas não combinam.")

    def test_user_email_already_exist(self):
        """
        Testando o caso que já existe um usuário com o email passado.
        """

        self.data['email'] = "fulano01@gmail.com"
        self.client.force_authenticate(self.superuser)
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get('detail'), "Já existe um usuário com esse email")
