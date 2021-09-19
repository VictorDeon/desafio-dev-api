from rest_framework import serializers
from .models import CNAB, Store


class StoreSerializer(serializers.Serializer):
    """
    Serialização dos dados das lojas e seus CNABs.
    """

    transaction_type = serializers.CharField(
        label="Tipo",
        help_text="Tipos de transações. Ex: Aluguel",
        error_messages={
            "required": "O tipo de transação é obrigatório",
            "blank": "O tipo de transação não pode está em branco."
        }
    )

    transaction_signal = serializers.CharField(
        label="Sinal",
        help_text="Sinal de operação da transação. Ex: + ou -",
        error_messages={
            "required": "O sinal da transação é obrigatório",
            "blank": "O sinal da transação não pode está em branco."
        }
    )

    date = serializers.CharField(
        label="Data",
        help_text="Data da ocorrência da transação",
        error_messages={
            "required": "A data da transação é obrigatória",
            "blank": "A data da transação não pode está em branco."
        }
    )

    value = serializers.CharField(
        label="Valor",
        help_text="Valor da movimentação.",
        error_messages={
            "required": "O valor da movimentação é obrigatório",
            "blank": "O valor da movimentação não pode está em branco."
        }
    )

    cpf = serializers.CharField(
        label="CPF",
        help_text="CPF do beneficiário",
        error_messages={
            "required": "O CPF do beneficiário é obrigatório",
            "blank": "O CPF do beneficiário não pode está em branco."
        }
    )

    card = serializers.CharField(
        label="Cartão",
        help_text="Cartão utilizado na transação",
        error_messages={
            "required": "O Cartão utilizado na transação é obrigatório",
            "blank": "O Cartão utilizado na transação não pode está em branco."
        }
    )

    time = serializers.CharField(
        label="Hora da ocorrência",
        help_text="Hora da ocorrência atendendo ao fuso de UTC-3",
        error_messages={
            "required": "A hora da ocorrência é obrigatório",
            "blank": "A hora da ocorrência não pode está em branco."
        }
    )

    owner = serializers.CharField(
        label="Nome",
        help_text="Nome do representante da loja",
        error_messages={
            "required": "O nome do representante da loja é obrigatório",
            "blank": "O nome do representante da loja não pode está em branco."
        }
    )

    store = serializers.CharField(
        label="Loja",
        help_text="Nome da loja",
        error_messages={
            "required": "O nome da loja é obrigatório",
            "blank": "O nome da loja não pode está em branco."
        }
    )

    def to_representation(self, instance):
        """
        Formata os dados de saída.
        """

        signal_map = {"+": 1, "-": -1}

        return {
            "title": instance.title,
            "cpf": instance.cpf,
            "owner": instance.owner,
            "total": round(float(sum([cnab.value * signal_map[cnab.transaction_signal] for cnab in instance.cnabs.all()])), 2),
            "cnabs": [{
                "transaction_type": cnab.transaction_type,
                "transaction_signal": cnab.transaction_signal,
                "date": cnab.date.strftime("%d/%m/%Y"),
                "value": round(float(cnab.value), 2),
                "card": cnab.card,
                "time": cnab.time.strftime("%H:%M:%S")
            } for cnab in instance.cnabs.all()]
        }

    def create(self, validated_data):
        """
        Cria as instâncias
        """

        store, created = Store.objects.get_or_create(
            title=validated_data['store'],
            defaults={
                "user": self.context.get('user'),
                "cpf": validated_data['cpf'],
                "owner": validated_data['owner']
            }
        )

        CNAB.objects.create(
            store=store,
            transaction_type=validated_data['transaction_type'],
            transaction_signal=validated_data['transaction_signal'],
            date=validated_data['date'],
            value=validated_data['value'],
            card=validated_data['card'],
            time=validated_data['time']
        )

        return store
