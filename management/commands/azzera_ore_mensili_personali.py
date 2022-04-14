from django.core.management.base import BaseCommand, CommandError
import datetime
from turni.models import *
from dateutil.relativedelta import *
from APIauth.models import User


class Command(BaseCommand):
    help = 'Promemoria permessi'

    def handle(self, *args, **options):
        '''
        Questo script azzera il primo del mese le ore mensili (dato salvato all'interno dell'utente stesso)
        lavorate dall'utente e calcolate giorno per giorno dall'API.
        '''

        print("INIZIO")
        users = User.objects.all()
        for u in users:
            u.ore_mese_attuale_lavorate = 0
            u.ultimo_aggiornamento_ore_mese_lavorate = datetime.datetime.now()
            u.save()
        print("FINE")
