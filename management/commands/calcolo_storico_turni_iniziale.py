from django.core.management.base import BaseCommand, CommandError
import datetime
from turni.models import *
from dateutil.relativedelta import *
from APIauth.models import User


class Command(BaseCommand):
    help = 'Promemoria permessi'

    def handle(self, *args, **options):
        print("INIZIO")
        data_inizio = datetime.date(2018, 1, 1)
        data_oggi = datetime.date.today()
        data_fine = datetime.date(data_oggi.year, data_oggi.month, 1)

        while data_inizio < data_fine:
            print(data_inizio)
            data_fine_mese = data_inizio + relativedelta(months=1) - relativedelta(days=1)

            for u in User.objects.all():
                print(u.email)
                totale_ore_mese_attuale = 0

                turno_mese_attuale = Turno.objects.filter(data__gte=data_inizio, data__lte=data_fine_mese, utente=u)
                for t in turno_mese_attuale:
                    totale_ore_mese_attuale += t.ore_impiegate

                # if non esiste lo storico
                if totale_ore_mese_attuale > 0:
                    try:
                        storico = StoricoTurno.objects.get(utente=u, mese=data_inizio)
                    except Exception:
                        storico = StoricoTurno(utente=u, mese=data_inizio)

                    storico.ore_impiegate = totale_ore_mese_attuale
                    storico.save()

            data_inizio = data_inizio + relativedelta(months=1)
