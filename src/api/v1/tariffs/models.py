from django.db import models
from django.core.validators import MinValueValidator

from api.v1.accounts.models import CustomUser
from api.v1.products.models import Product
from .enums import AdvantageType
from .services import upload_tariff_path


class Advantage(models.Model):
    creator = models.ForeignKey(CustomUser, related_name='advantges', on_delete=models.SET_NULL, null=True)
    advantage_type = models.CharField(max_length=1, choices=AdvantageType.choices())
    value = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    price = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.value} {self.type}'

class Tariff(models.Model):
    creator = models.ForeignKey(CustomUser, related_name='tariffs', on_delete=models.SET_NULL, null=True)
    advantages = models.ManyToManyField(Advantage)

    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to=upload_tariff_path)
    optimal = models.BooleanField(default=False)
    price = models.FloatField(validators=[MinValueValidator(1000)])
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductTariff(models.Model):
    product = models.ForeignKey(Product, related_name='tariffs', on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, related_name='tariffs', on_delete=models.PROTECT)
    advantages = models.ManyToManyField(Advantage, blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tariff