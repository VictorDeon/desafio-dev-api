from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User
from ..models import CNAB, Store


class GetUserTestCase(APITestCase):
    """
    Testes unitários para verificar o comportamento
    de extração dos dados do CNAB
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
            name='Fulano',
            email='fulano@gmail.com',
            password='django1234'
        )

        self.cnab = open("./apps/cnab/tests/CNAB.txt", "rb")

    def tearDown(self):
        """
        Executado após cada teste.
        """

        self.cnab.seek(0)
        self.cnab.close()
        Store.objects.all().delete()
        CNAB.objects.all().delete()
        User.objects.all().delete()
        self.client.logout()

    def test_get_cnab_by_admin_user(self):
        """
        Administrador armazenar dados de CNAB
        """

        url = reverse('cnab-upload')
        self.client.force_authenticate(self.superuser)
        self.assertEqual(CNAB.objects.count(), 0)
        self.assertEqual(Store.objects.count(), 0)
        response = self.client.post(url, data={ "file": self.cnab }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(Store.objects.count(), 5)
        self.assertEqual(CNAB.objects.count(), len(response.data['results']))
