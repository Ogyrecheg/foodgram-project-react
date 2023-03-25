from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    password = models.CharField(
        max_length=32,
        verbose_name='пароль',
        blank=True,
        null=True,
    )
