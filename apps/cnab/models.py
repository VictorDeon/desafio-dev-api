from django.db import models
from .enum import TransactionType


class CNAB(models.Model):
    """
    Modelo de CNAB
    """

    cpf = models.CharField(max_length=14)

    owner = models.CharField(max_length=14)

    store = models.CharField(max_length=19)

    transaction_type = models.CharField(max_length=50, choices=TransactionType.choices)

    transaction_signal = models.CharField(max_length=1)

    date = models.DateField()

    value = models.DecimalField(max_digits=9, decimal_places=3, default=0.0)

    card = models.CharField(max_length=12)

    time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Representação da modelo como string.
        """

        return f"{self.store} - R$ {self.value}"

    class Meta:
        """
        Informações adicionais do modelo.
        """

        db_table = "cnab"
        ordering = ('-date', '-time')
