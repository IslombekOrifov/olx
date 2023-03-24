from django.db import models

from api.v1.accounts.models import CustomUser
from api.v1.products.models import Product


class MainComplaint(models.Model):
    text = models.CharField(max_length=250)

    creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


    def save(self, *args, **kwargs):
        self.text = ' '.join(self.text.strip().split())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.text


class Complaint(models.Model):
    text = models.CharField(max_length=250)

    client = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    mcomplaint = models.ForeignKey(MainComplaint, on_delete=models.PROTECT)

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.text = ' '.join(self.text.strip().split())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.mcomplaint} -> {self.text}"