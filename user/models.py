from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models


class CustomUser(AbstractUser):
    MALE_CHOIСES = (
        ("None", "Не выбрано"),
        ("man", "Мужчина"),
        ("woman", "Женщина"),
    )
    phone = models.CharField(null=True, blank=True, max_length=50, default='+')
    date_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(
        max_length=30,
        null=True,
        choices=MALE_CHOIСES,
    )
    points = models.CharField(max_length=150, verbose_name='points', null=True)
    address = models.CharField(max_length=169, verbose_name='address', null=True)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
