from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo de e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    MAX_LENGTH_USER_NAME = 200
    MAX_LENGTH_EMAIL = 200
    MAX_LENGTH_NAME = 60

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    USERNAME_FIELD = 'email'

    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(
        u'Primeiro nome', max_length=MAX_LENGTH_NAME, blank=True, null=True)
    last_name = models.CharField(
        u'Último nome', max_length=60, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    @property
    def get_full_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def __str__(self):
        return self.get_full_name


class IdentityClient(models.Model):
    class Meta:
        verbose_name = 'Cliente de identidade'
        verbose_name_plural = 'Clientes de identidade'

    name = models.CharField(max_length=255)
    app_id = models.CharField(max_length=40, unique=True)
    api_key = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f'{self.name}'
