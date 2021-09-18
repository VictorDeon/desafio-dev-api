from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.views import status
from rest_framework.response import Response
from shared.exception import GenericException
from .permissions import RetrieveLoggedPermission
from .enum import TransactionType, TransactionSignal


class CNABViewSet(ViewSet):
    """
    View set do modelo de Resultado de simulação
    """

    permission_classes = (RetrieveLoggedPermission,)
    path = "./apps/cnab/CNAB.txt"

    def __open_file(self):
        """
        Abre o arquivo de forma async.
        """

        lines = []
        with open(self.path, "r") as f:
            for line in f.readlines():
                lines.append(line)

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

    @action(detail=False, methods=['get'], url_path="cnab", url_name="cnab")
    def cnab(self, request):
        """
        Extrai os dados do CNAB e armazena no banco
        """

        lines = self.__open_file()

        results = []
        for line in lines:
            data = self.__extract_data_from_line(line)
            results.append(data)

        return Response({ "success": True, "results": results }, status=status.HTTP_200_OK)
