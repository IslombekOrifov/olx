import sys
import random 

from django.core.management.base import BaseCommand, CommandError

from api.v1.accounts.models import CustomUser
from api.v1.products.models import Category, Product, Field

class Command(BaseCommand):
    
    def handle(self, count=1000, *args, **options):
        categories = Category.objects.filter(children__isnull=True)
        creator = CustomUser.objects.filter(is_staff=True).last()
       
        # a = list((Field(name=f'field dummy with management command {random.randint(1, 11000000)}', creator=creator) for i in categories))
        # Field.objects.bulk_create(a)
        # print('done')
        i = 0
        for cat in categories:
            i += 1
            cat.field_set.add(*list((field for field in Field.objects.all()[i*5:][:i*10])))
        

        print('done')
