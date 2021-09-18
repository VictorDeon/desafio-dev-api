from django.db import models
from .enum import TransactionType


class Store(models.Model):
    """
    Modelo da loja.
    """

    store = models.CharField(max_length=19, unique=True)

    cpf = models.CharField(max_length=14)

    owner = models.CharField(max_length=14)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Representação da modelo como string.
        """

        return self.store

    class Meta:
        """
        Informações adicionais do modelo.
        """

        db_table = "store"
        ordering = ('-created_at',)

class CNAB(models.Model):
    """
    Modelo de CNAB
    """

    store = models.ForeignKey(
        Store,
        verbose_name='Loja',
        related_name="cnabs",
        on_delete=models.CASCADE
    )

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
