from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models


class AddressInfoModel(models.Model):
    lat = models.DecimalField(max_digits=40, decimal_places=10)
    lng = models.DecimalField(max_digits=40, decimal_places=10)


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
    address = models.CharField(max_length=169, verbose_name='address', null=True)
    address_coordinates = models.ForeignKey(AddressInfoModel, on_delete=models.PROTECT, null=True)
    is_house = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
