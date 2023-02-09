from django.db import models

from api.v1.accounts.models import CustomUser
from api.v1.products.models import Product
from .services import upload_chat_message_path


class Message(models.Model):
    product = models.ForeignKey(Product, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='messages', blank=True, null=True, on_delete=models.CASCADE)
    
    body = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to=upload_chat_message_path, blank=True)

    is_client_message = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-date_created',)
    
    def __str__(self):
        return f"{self.chat.product.title} -> {self.user.email}"
    

