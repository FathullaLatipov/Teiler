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
    email = models.EmailField(blank=True, null=True)
    sex = models.CharField(
        max_length=30,
        null=True,
        choices=MALE_CHOIСES,
    )
    points = models.CharField(max_length=150, verbose_name='points', null=True)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class AdressInfoModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True)
    address = models.CharField(max_length=169, verbose_name='address', null=True)
    lat = models.FloatField(max_length=50, null=True)
    lng = models.FloatField(max_length=50, null=True)
    is_house = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

