# Generated by Django 3.2 on 2023-02-14 13:19

import api.v1.products.services
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to=api.v1.products.services.upload_category_path)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('is_filter', models.BooleanField(default=False)),
                ('is_main', models.BooleanField(default=False)),
                ('is_checkbox', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(to='products.Category')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_fields', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(20)])),
                ('description', models.TextField(max_length=9000, validators=[django.core.validators.MinLengthValidator(80)])),
                ('region', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('image_main', models.ImageField(blank=True, null=True, upload_to=api.v1.products.services.upload_product_path)),
                ('image1', models.ImageField(blank=True, null=True, upload_to=api.v1.products.services.upload_product_path)),
                ('image2', models.ImageField(blank=True, null=True, upload_to=api.v1.products.services.upload_product_path)),
                ('image3', models.ImageField(blank=True, null=True, upload_to=api.v1.products.services.upload_product_path)),
                ('image4', models.ImageField(blank=True, null=True, upload_to=api.v1.products.services.upload_product_path)),
                ('image5', models.ImageField(blank=True, null=True, upload_to=api.v1.products.services.upload_product_path)),
                ('image6', models.ImageField(blank=True, null=True, upload_to=api.v1.products.services.upload_product_path)),
                ('image7', models.ImageField(blank=True, null=True, upload_to=api.v1.products.services.upload_product_path)),
                ('price', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('price_is_dollar', models.BooleanField(default=False)),
                ('exchange', models.BooleanField(default=False)),
                ('negotiable', models.BooleanField(default=False)),
                ('product_condition', models.BooleanField(default=True)),
                ('auto_renewal', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, max_length=13)),
                ('views_count', models.PositiveSmallIntegerField(default=0)),
                ('status', models.CharField(choices=[('wt', 'Waiting'), ('ac', 'Active'), ('na', 'Not Active'), ('rd', 'Rejected'), ('ar', 'Archive'), ('bn', 'Banned')], default='wt', max_length=3)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=255)),
                ('is_true', models.BooleanField(default=False)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.field')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat_fields', to='products.product')),
            ],
        ),
    ]
