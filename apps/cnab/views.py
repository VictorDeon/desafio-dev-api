from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.views import status
from rest_framework.response import Response
from shared.exception import GenericException
from .models import CNAB, Store
from .permissions import RetrieveLoggedPermission
from .enum import TransactionType, TransactionSignal


class CNABViewSet(ViewSet):
    """
    View set do modelo de Resultado de simulação
    """

    permission_classes = (RetrieveLoggedPermission,)

    def __open_file(self, data):
        """
        Abre o arquivo de forma async.
        """

        lines = []
        for line in data['file'].readlines():
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

        transaction = line[0:1]

        result = {
            "transaction_type": transaction_map[transaction]["type"],
            "transaction_signal": transaction_map[transaction]["signal"],
            "date": f"{line[1:5]}-{line[5:7]}-{line[7:9]}",
            "value": round(float(line[9:19]) / 100, 2),
            "cpf": f"{line[19:22]}.{line[22:25]}.{line[25:28]}-{line[28:30]}",
            "card": line[30:42],
            "time": f"{line[42:44]}:{line[44:46]}:{line[46:48]}",
            "owner": line[48:62].strip(),
            "store": line[62:].strip().replace("\n", "")
        }

        return result

    def __create_stores_and_cnabs(self, results):
        """
        Cria as lojas e cnabs
        """

        for result in results:
            store, created = Store.objects.get_or_create(
                store=result['store'],
                defaults={ "cpf": result['cpf'], "owner": result['owner'] }
            )

            CNAB.objects.create(
                store=store,
                transaction_type=result['transaction_type'],
                transaction_signal=result['transaction_signal'],
                date=result['date'],
                value=result['value'],
                card=result['card'],
                time=result['time']
            )


    @action(detail=False, methods=['post'], url_path="cnab", url_name="upload")
    def cnab(self, request, *args, **kwargs):
        """
        Extrai os dados do CNAB e armazena no banco
        """

        lines = self.__open_file(request.data)

        results = []
        for line in lines:
            data = self.__extract_data_from_line(line)
            results.append(data)

        self.__create_stores_and_cnabs(results)

        return Response({ "success": True, "results": results }, status=status.HTTP_200_OK)
