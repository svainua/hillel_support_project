from django.contrib.auth.models import (  # основу для класса User взяли из auth или models. #noqa
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import (  # https://docs.djangoproject.com/en/5.0/topics/db/models/   #noqa
    models,
)
from django.utils import timezone

from .enums import Role
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    role = models.CharField(
        max_length=20, default=Role.JUNIOR, choices=Role.choices()
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    date_joined = models.DateTimeField(
        default=timezone.now
    )  # когда зарегистрировались

    objects = (
        UserManager()
    )  # инкапсулирует инфо по работе с БД. Это и есть реализация ОРМ. В ней есть функции по работе с таблицами #noqa

    EMAIL_FIELD = "email"
    # USERNAME_FIELD = "username"  # если для регистр нужно только емейл и пароль, то емейл будет юзернеймом  #noqa
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]
    REQUIRED_FIELDS = []  # не задаем обязательные поля

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between"""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return self.email
