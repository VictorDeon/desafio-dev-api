from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.views import status
from rest_framework.response import Response
from shared.exception import GenericException
from .permissions import RetrieveLoggedPermission
from .enum import TransactionType, TransactionSignal
from .serializers import StoreSerializer
from .models import Store


class CNABViewSet(ViewSet):
    """
    View set do modelo de Resultado de simulação
    """

    permission_classes = (RetrieveLoggedPermission,)
    serializer_class = StoreSerializer

    def __open_file(self, data):
        """
        Abre o arquivo de forma async.
        """

        if data['file'].content_type != "text/plain":
            raise GenericException(
                "Formato de arquivo inválido, deve ser do tipo text/plain.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        lines = []
        for line in data['file'].readlines():
            if len(line.decode()) != 81:
                raise GenericException(
                    "O tamanho de cada linha do cnab deve conter exatamente 81 caracteres.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            lines.append(line.decode())

        data['file'].close()

        return lines

    def __extract_data_from_line(self, line):
        """
        Extrai os dados por linha.
        """

        transaction_map = {
            "1": {"type": TransactionType.DEBIT.value, "signal": TransactionSignal.DEBIT.value},
            "2": {"type": TransactionType.BILL.value, "signal": TransactionSignal.BILL.value},
            "3": {"type": TransactionType.FINANCING.value, "signal": TransactionSignal.FINANCING.value},
            "4": {"type": TransactionType.CREDIT.value, "signal": TransactionSignal.CREDIT.value},
            "5": {"type": TransactionType.RECEIVEMENT.value, "signal": TransactionSignal.RECEIVEMENT.value},
            "6": {"type": TransactionType.SALES.value, "signal": TransactionSignal.SALES.value},
            "7": {"type": TransactionType.TED.value, "signal": TransactionSignal.TED.value},
            "8": {"type": TransactionType.DOC.value, "signal": TransactionSignal.DOC.value},
            "9": {"type": TransactionType.RENT.value, "signal": TransactionSignal.RENT.value},
        }

        result = {
            "transaction_type": transaction_map[line[0:1]]["type"],
            "transaction_signal": transaction_map[line[0:1]]["signal"],
            "date": f"{line[1:5]}-{line[5:7]}-{line[7:9]}",
            "value": round(float(line[9:19]) / 100, 2),
            "cpf": f"{line[19:22]}.{line[22:25]}.{line[25:28]}-{line[28:30]}",
            "card": line[30:42],
            "time": f"{line[42:44]}:{line[44:46]}:{line[46:48]}",
            "owner": line[48:62].strip(),
            "store": line[62:].strip().replace("\n", "")
        }

        return result

    def __create_stores_and_cnabs(self, user, cnabs):
        """
        Cria as lojas e cnabs
        """

        for cnab in cnabs:
            serializer = StoreSerializer(data=cnab, context={"user": user})
            if serializer.is_valid():
                serializer.save()

    def __to_representation(self):
        """
        Formata os dados de saída.
        """

        results = []
        stores = Store.objects.all()
        for store in stores:
            serializer = StoreSerializer()
            results.append(serializer.to_representation(store))

        return results

    @action(detail=False, methods=['post'], url_path="cnab", url_name="upload")
    def cnab(self, request, *args, **kwargs):
        """
        Extrai os dados do CNAB e armazena no banco
        """

        lines = self.__open_file(request.data)

        cnabs = []
        for line in lines:
            data = self.__extract_data_from_line(line)
            cnabs.append(data)

        self.__create_stores_and_cnabs(request.user, cnabs)

        return Response(
            {"success": True, "results": self.__to_representation()},
            status=status.HTTP_200_OK
        )
