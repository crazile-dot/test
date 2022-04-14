from django.core.management.base import BaseCommand, CommandError
import datetime
from turni.models import *
from dateutil.relativedelta import *
from APIauth.models import User
from email.mime.text import MIMEText
from django.conf import settings

import smtplib

def mail_sending(m):
    s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    s.starttls()
    s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    s.send_message(m)
    s.quit()

class Command(BaseCommand):
    help = 'Promemoria permessi'

    def handle(self, *args, **options):
        data_oggi = datetime.date.today()
        data_inizio_appoggio = data_oggi - relativedelta(months=1)
        data_inizio = datetime.date(data_inizio_appoggio.year, data_inizio_appoggio.month, 1)
        for u in User.objects.all():
            tot_mensile = int(u.fascia_oraria_mensile)*4
            turno_mese_attuale = Turno.objects.filter(data__gte=data_inizio, data__lte=data_oggi, utente=u)
            totale_ore_mese_attuale = 0
            for t in turno_mese_attuale:
                totale_ore_mese_attuale += t.ore_impiegate

            # if non esiste lo storico
            if totale_ore_mese_attuale > 0:
                if totale_ore_mese_attuale < tot_mensile:
                    ore_rimaste = tot_mensile - totale_ore_mese_attuale
                    if ore_rimaste > 10:
                        nome = u.username
                        mail = u.email
                        testo_mail = "Caro %s ti mancano ancora %d ore per svolgere appieno il tuo dovere, che dici ci diamo una mossa?" %(nome, ore_rimaste)
                        m = MIMEText(testo_mail, 'html')
                        m['Subject'] = 'Promemoria turno %s' % nome
                        m['From'] = settings.EMAIL_HOST_USER
                        m['To'] = mail + "," + settings.EMAIL_HOST_USER
                        mail_sending(m)
                        print(m)
                    else:
                        nome = u.username
                        mail = u.email
                        testo_mail = "Dai %s ti mancano solo %d ore per svolgere appieno il tuo dovere, Grande!" %(nome, ore_rimaste)
                        m = MIMEText(testo_mail, 'html')
                        m['Subject'] = 'Promemoria turno %s' % nome
                        m['From'] = settings.EMAIL_HOST_USER
                        m['To'] = mail + "," + settings.EMAIL_HOST_USER
                        mail_sending(m)
                        print(m)