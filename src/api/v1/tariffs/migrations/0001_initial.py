# Generated by Django 3.2 on 2023-02-14 13:19

import api.v1.tariffs.services
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advantage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advantage_type', models.CharField(choices=[('t', 'TOP'), ('u', 'UP'), ('v', 'VIP')], max_length=1)),
                ('value', models.PositiveSmallIntegerField(default=1)),
                ('price', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='advantages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=api.v1.tariffs.services.upload_tariff_path)),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('optimal', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('advantages', models.ManyToManyField(to='tariffs.Advantage')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tariffs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductTariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('advantages', models.ManyToManyField(blank=True, to='tariffs.Advantage')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tariffs', to='products.product')),
                ('tariff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tariffs', to='tariffs.tariff')),
            ],
        ),
    ]
