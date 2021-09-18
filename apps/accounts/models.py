from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Gerenciamento de objetos da classe.
    """

    def create_user(self, email, name, password):
        """
        Cria um usuário comum.
        """

        email = self.normalize_email(email)

        user = self.model(email=email, name=name)

        # Criptografia do password
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """
        Cria um usuário do tipo staff.
        """

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário para autorização e autenticação.
    """

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # O campo que será usado para autenticação
    USERNAME_FIELD = 'email'

    # É uma lista de campos necessários para todos os usuários,
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        """
        Representação da modelo como string.
        """

        return self.email

    class Meta:
        """
        Informações adicionais do modelo.
        """

        db_table = "accounts_users"
        ordering = ('-created_at',)
