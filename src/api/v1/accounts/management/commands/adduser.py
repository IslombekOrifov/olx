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
                username=f'user{_}', email=f'user{_}@gmail.com', password=f'userpass{_}'
            )