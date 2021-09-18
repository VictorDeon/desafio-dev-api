from django.db import models
from enum import Enum


class TransactionType(models.TextChoices):
    """
    Mapeando as transações
    """

    DEBIT = "Débito"
    BILL = "Boleto"
    FINANCING = "Financiamento"
    CREDIT = "Crédito"
    RECEIVEMENT = "Recebimento Empréstimo"
    SALES = "Vendas"
    TED = "Recebimento TED"
    DOC = "Recebimento DOC"
    RENT = "Aluguel"


class TransactionSignal(Enum):
    """
    Mapeia o sinal de sainda de cada transação.
    """

    DEBIT = "+"
    BILL = "-"
    FINANCING = "-"
    CREDIT = "+"
    RECEIVEMENT = "+"
    SALES = "+"
    TED = "+"
    DOC = "+"
    RENT = "-"
