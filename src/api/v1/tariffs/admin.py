from django.contrib import admin

from .models import Advantage, Tariff, ProductTariff


admin.site.register([Advantage, Tariff, ProductTariff])
