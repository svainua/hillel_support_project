from django.db import (
    models,  # https://docs.djangoproject.com/en/5.0/topics/db/models/
)


class User(models.Model):  # наследуем класс Model()
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=10)
