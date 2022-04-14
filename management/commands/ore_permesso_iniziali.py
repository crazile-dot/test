from django.core.management.base import BaseCommand
from APIauth.models import User

# da eseguire solo la prima volta, poi si può anche cancellare
class Command(BaseCommand):
    help = 'set iniziale permessi'
    def handle(self, *args, **options):
        for u in User.objects.all():
            ore_mensili = int(u.fascia_oraria_mensile)*4
            u.ore_permesso_accumulate = (ore_mensili/8)*2
            u.save()