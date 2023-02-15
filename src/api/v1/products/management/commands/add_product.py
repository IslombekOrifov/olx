import sys
import random 

from django.core.management.base import BaseCommand, CommandError

from api.v1.accounts.models import CustomUser
from api.v1.products.models import Category, Product

class Command(BaseCommand):
    
    def handle(self, count=1000, *args, **options):
        desc = """fringilla ut morbi tincidunt augue interdum velit euismod 
            in pellentesque massa placerat duis ultricies lacus sed turpis tincidunt 
            id aliquet risus feugiat in ante metus dictum at tempor commodo ullamcorper 
            a lacus vestibulum sed arcu non odio euismod lacinia at quis risus sed 
            vulputate odio ut enim blandit volutpat maecenas volutpat blandit aliquam 
            etiam erat velit scelerisque in dictum non consectetur a erat nam at lectus 
            urna duis convallis convallis tellus id interdum velit laoreet id donec 
            ultrices tincidunt arcu
        """
        categories = Category.objects.filter(children__isnull=True)
        creators = CustomUser.objects.filter(is_staff=False)
        regions = [
            'Andijan', 'Bukhara', 'Djizzak', 'Fergana', 'Kashkadarya', 'Khorezm',
            'Namangan', 'Navoi', 'Samarkand', 'Surkhandarya', 'Syrdarya', 'Tashkent',]
        for _ in creators:
            for i in categories:
                if i.id % 5 == 0:
                    Product.objects.create(
                        title=f'Product dummy with management command {random.randint(1, 11000000)}', 
                        author=_, category=i, description=desc, region=random.choice(regions), 
                        district=random.choice(regions)
                    )
                elif i.id % 2 == 0:
                    Product.objects.create(
                        title=f'Product dummy with management command {random.randint(1, 11000000)}', 
                        author=_, category=i, description=desc, region=random.choice(regions), 
                        district=random.choice(regions), price=round(random.uniform(10000.00, 10000000.00), 2),
                        negotiable=True
                    )
                else:
                    Product.objects.create(
                        title=f'Product dummy with management command {random.randint(1, 11000000)}', 
                        author=_, category=i, description=desc, region=random.choice(regions), 
                        district=random.choice(regions), exchange=True
                    )