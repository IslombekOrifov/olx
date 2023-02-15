import sys


from django.core.management.base import BaseCommand, CommandError
from api.v1.accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Add users'
    args = '[count]'

    def handle(self, count=1000, *args, **options):

        try:
            i = int(count)
        except ValueError:
            print(u'n is to be a number!')
            sys.exit(1)

        for _ in range(i):
            # you can pass params explicitly
            CustomUser.objects.create_user(
                username=f'aaa{_}', email=f'aaa{_}@gmail.com', password=f'aaa{_}'
            )