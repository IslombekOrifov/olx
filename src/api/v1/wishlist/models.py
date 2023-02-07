from django.db import models

from api.v1.accounts.models import CustomUser
from api.v1.products.models import Product


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, related_name='wishlists', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlists', on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, related_name='follows', on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)