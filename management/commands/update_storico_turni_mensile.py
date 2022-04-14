from django.core.management.base import BaseCommand, CommandError
import datetime
from turni.models import *
from dateutil.relativedelta import *
from APIauth.models import User


class Command(BaseCommand):
    help = 'Promemoria permessi'

    def handle(self, *args, **options):
        '''
        Questo script calcola mese per mese, utente per utente, la somma delle ore di tutti i suoi turni
        lavorati nel mese precedente al lancio dello script stesso.
        Verrà impostato di default al 5 di ogni mese. Quindi ad esempio il 5 di Febbraio eseguirà la somma per il
        report dei turni di Gennaio.
        '''

        print("INIZIO")
        data_oggi = datetime.date.today()

        data_inizio_appoggio = data_oggi - relativedelta(months=1)
        data_inizio = datetime.date(data_inizio_appoggio.year, data_inizio_appoggio.month, 1)

        data_fine = data_inizio + relativedelta(months=1) - relativedelta(days=1)

        print(data_inizio, data_fine)

        while data_inizio < data_fine:
            print(data_inizio)
            data_fine_mese = data_inizio + relativedelta(months=1) - relativedelta(days=1)
            for u in User.objects.all():
                print(u.email)
                fascia_oraria = int(u.fascia_oraria_mensile)
                permesso = fascia_oraria/2
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
                    # if totale_ore_mese_attuale >= (fascia_oraria*4) - permesso:
                    #     u.permission += (totale_ore_mese_attuale - ((fascia_oraria*4) - permesso))
                    # else:
                    #     u.permission = (u.permission - (fascia_oraria*4) - permesso-totale_ore_mese_attuale)
            data_inizio = data_inizio + relativedelta(months=1)
            # print(u.permission)
