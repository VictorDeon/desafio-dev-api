from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from apps.accounts.models import User
from ..models import CNAB, Store
from ..views import CNABViewSet
from ..enum import TransactionType, TransactionSignal
from ..serializers import StoreSerializer


class GetUserTestCase(APITestCase):
    """
    Testes unitários para verificar o comportamento
    de extração dos dados do CNAB
    """

    def setUp(self):
        """
        Roda antes de cada método.
        """

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

    def test_get_cnab_by_user(self):
        """
        Testando o fluxo de envio do cnab e armazenamento
        do mesmo no BD.
        """

        url = reverse('cnab-upload')
        self.client.force_authenticate(self.user)
        self.assertEqual(CNAB.objects.count(), 0)
        self.assertEqual(Store.objects.count(), 0)
        response = self.client.post(url, data={"file": self.cnab}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(Store.objects.last().user, self.user)
        self.assertEqual(Store.objects.count(), len(response.data['results']))
        self.assertEqual(CNAB.objects.count(), 21)

    def test_cnab_line_formater(self):
        """
        Testando a transformação de uma linha do qnab em objeto
        para armazenar no banco.
        """

        line = "3201903010000014200096206760174753****3153153453JOÃO MACEDO   BAR DO JOÃO"
        formated_data = CNABViewSet()._CNABViewSet__extract_data_from_line(line)
        self.assertEqual(formated_data, {
            "transaction_type": TransactionType.FINANCING.value,
            "transaction_signal": TransactionSignal.FINANCING.value,
            "date": "2019-03-01",
            "value": 142.0,
            "cpf": "096.206.760-17",
            "card": "4753****3153",
            "time": "15:34:53",
            "owner": "JOÃO MACEDO",
            "store": "BAR DO JOÃO"
        })

    def test_not_get_cnab_by_not_logged_user(self):
        """
        Usuário não autenticado não pode fazer upload do cnab
        """

        url = reverse('cnab-upload')
        self.assertEqual(CNAB.objects.count(), 0)
        self.assertEqual(Store.objects.count(), 0)
        response = self.client.post(url, data={"file": self.cnab}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail'), "Usuário precisa esta autenticado para realizar essa ação!")
        self.assertEqual(CNAB.objects.count(), 0)
        self.assertEqual(Store.objects.count(), 0)

    def test_not_get_cnab_invalid_file(self):
        """
        Não pode enviar um arquivo que seja diferente de text/plain.
        """

        self.cnab.close()
        self.cnab = open("./apps/cnab/tests/gateways.png", "rb")
        self.client.force_authenticate(self.user)
        url = reverse('cnab-upload')
        self.assertEqual(CNAB.objects.count(), 0)
        self.assertEqual(Store.objects.count(), 0)
        response = self.client.post(url, data={"file": self.cnab}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), "Formato de arquivo inválido, deve ser do tipo text/plain.")
        self.assertEqual(CNAB.objects.count(), 0)
        self.assertEqual(Store.objects.count(), 0)

    def test_not_get_cnab_invalid_line_format(self):
        """
        O tamanho da linha do cnab não deve ser diferente de 81 caracteres.
        """

        self.cnab.close()
        self.cnab = open("./apps/cnab/tests/CNAB_wrong.txt", "rb")
        self.client.force_authenticate(self.user)
        url = reverse('cnab-upload')
        self.assertEqual(CNAB.objects.count(), 0)
        self.assertEqual(Store.objects.count(), 0)
        response = self.client.post(url, data={"file": self.cnab}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), "O tamanho de cada linha do cnab deve conter exatamente 81 caracteres.")
        self.assertEqual(CNAB.objects.count(), 0)
        self.assertEqual(Store.objects.count(), 0)

    def error_serializer_tests(self, field, msg):
        """
        Testa erros especificos de testes.
        """

        cnab = {f"{field}": ""}
        serializer = StoreSerializer(data=cnab, context={"user": self.user})
        self.assertFalse(serializer.is_valid())
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)
        if not serializer.is_valid():
            self.assertEqual(serializer.errors[f"{field}"][0], msg)

    def test_cnab_empty_transaction_type(self):
        """
        O tipo de transação não pode ser vazio.
        """

        self.error_serializer_tests("transaction_type", "O tipo de transação não pode está em branco.")

    def test_cnab_empty_transaction_signal(self):
        """
        O sinal da transação não pode ser vazio.
        """

        self.error_serializer_tests("transaction_signal", "O sinal da transação não pode está em branco.")

    def test_cnab_empty_value(self):
        """
        O sinal da transação não pode ser vazio.
        """

        self.error_serializer_tests("value", "O valor da movimentação não pode está em branco.")

    def test_cnab_empty_date(self):
        """
        A data de ocorrencia não pode ser vazio.
        """

        self.error_serializer_tests("date", "A data da transação não pode está em branco.")

    def test_cnab_empty_cpf(self):
        """
        O CFP não pode ser vazio.
        """

        self.error_serializer_tests("cpf", "O CPF do beneficiário não pode está em branco.")

    def test_cnab_empty_card(self):
        """
        O card não pode ser vazio.
        """

        self.error_serializer_tests("card", "O Cartão utilizado na transação não pode está em branco.")

    def test_cnab_empty_time(self):
        """
        A hora da ocorrência não pode ser vazio.
        """

        self.error_serializer_tests("time", "A hora da ocorrência não pode está em branco.")

    def test_cnab_empty_owner(self):
        """
        A hora da ocorrência não pode ser vazio.
        """

        self.error_serializer_tests("owner", "O nome do representante da loja não pode está em branco.")

    def test_cnab_empty_store(self):
        """
        A hora da ocorrência não pode ser vazio.
        """

        self.error_serializer_tests("store", "O nome da loja não pode está em branco.")
