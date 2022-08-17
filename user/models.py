from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    MALE_CHOIСES = (
        ("None", "Не выбрано"),
        ("Мужчина", "Мужчина"),
        ("Женщина", "Женщина"),
    )
    phone = models.PositiveIntegerField(null=True, blank=True)
    date_birth = models.DateField(null=True, blank=True)
    male = models.CharField(
        max_length=30,
        choices=MALE_CHOIСES,
        default=None,
        null=True,
        blank=True
    )
