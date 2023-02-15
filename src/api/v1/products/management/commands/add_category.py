import sys
import random 

from django.core.management.base import BaseCommand, CommandError

from api.v1.accounts.models import CustomUser
from api.v1.products.models import Category

class Command(BaseCommand):
    help = 'Add category children'

    def handle(self, *args, **options):
        categories = Category.objects.filter(parent__isnull=True)
        creator = CustomUser.objects.all().last()
        for _ in categories:
            for i in range(9):
                Category.objects.create(
                    name=f'ikkinchi{random.randint(1, 100)}', parent=_, creator=creator
                )

        categories = Category.objects.filter(parent__isnull=False) 
        for _ in categories:
            for j in range(9):
                        Category.objects.create(
                            name=f'uchinchi{random.randint(1, 100)}', parent=_, creator=creator
                        )