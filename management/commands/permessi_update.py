import datetime
import smtplib

from django.core.management.base import BaseCommand, CommandError
from domain_reminder.models import Reminder
from email.mime.text import MIMEText
from django.conf import settings
from domain_reminder.models import Reminder
from APIauth.models import User
from turni.models import Turno
from dateutil.relativedelta import *


def mail_sending(m):
    s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    s.starttls()
    s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    s.send_message(m)
    s.quit()

def expire_day_update(reminder):
    new_day = reminder.reminder_date.day
    new_month = reminder.reminder_date.month
    new_year = reminder.reminder_date.year + 1
    new_date = datetime.date(new_year, new_month, new_day)
    reminder.reminder_date = new_date
    reminder.save()

class Command(BaseCommand):
    help = 'Promemoria permessi'

    def handle(self, *args, **options):

        data_oggi = datetime.date.today()
        data_inizio_mese = datetime.date(data_oggi.year, data_oggi.month, 1)
        data_inizio_mese = data_inizio_mese - relativedelta(months=1)
        for u in User.objects.all():
            ore_mensili = int(u.fascia_oraria_mensile) * 4
            totale_ore_mese_attuale = 0
            u.ore_permesso_accumulate = float(u.ore_permesso_accumulate) + ore_mensili/8

            turno_mese_attuale = Turno.objects.filter(data__gte=data_inizio_mese, utente=u)
            for t in turno_mese_attuale:
                totale_ore_mese_attuale += t.ore_impiegate

            if ore_mensili < totale_ore_mese_attuale <= (ore_mensili + ore_mensili*6/8):
                u.ore_permesso_accumulate += (totale_ore_mese_attuale - ore_mensili)
            else:
                if (ore_mensili/2) <= totale_ore_mese_attuale < ore_mensili:
                    u.ore_permesso_accumulate -= (ore_mensili - totale_ore_mese_attuale)
                else:
                    if totale_ore_mese_attuale == ore_mensili:
                        continue
                    else:
                        if totale_ore_mese_attuale < (ore_mensili/2):
                            u.ore_permesso_accumulate -= (ore_mensili - totale_ore_mese_attuale)
                            # ed invia mail con cazziatone
                        else:
                            if totale_ore_mese_attuale > (ore_mensili + ore_mensili*6/8):
                                #invia mail con cazziatone
                                continue

            today = datetime.date.today()
            expire_day = today + relativedelta(months=1)

            '''
            # da qui in poi gestisce solo l'invio delle mail
            if totale_ore_mese_attuale > (ore_mensili + ore_mensili*6/8):
                reminder = Reminder.objects.filter(reminder_date__gte=today, reminder_date__lte=expire_day,reminder_boolean = False)
                for r in reminder:
                    nome = r.reminder_name
                    mail = r.reminder_mail
                    dominio = r.reminder_domain
                    testo_mail = "Buonasera %s,<br><br>" "Hai superato di %d ore il tetto massimo. Per questo mese basta lavorare :)" % (
                        nome, totale_ore_mese_attuale-(ore_mensili + ore_mensili*6/8))
                    m = MIMEText(testo_mail, 'html')
                    m['Subject'] = 'Resoconto ore lavorate nel mese %s' % nome
                    m['From'] = settings.EMAIL_HOST_USER
                    m['To'] = mail + "," + settings.EMAIL_HOST_USER
                    mail_sending(m)
                    print (r.reminder_mail)
                    r.reminder_boolean = True
                    r.save()
            else:
                if (ore_mensili*0.5) > totale_ore_mese_attuale:
                    reminder = Reminder.objects.filter(reminder_date__gte=today, reminder_date__lte=expire_day, reminder_boolean=False)
                    for r in reminder:
                        nome = r.reminder_name
                        mail = r.reminder_mail
                        dominio = r.reminder_domain
                        testo_mail = "Buonasera %s,<br><br>" "Sembra che tu sia nei guai! Hai lavorato %d ore in meno rispetto al minimo mensile previsto." % (
                        nome, (ore_mensili*0.5 - totale_ore_mese_attuale))
                        m = MIMEText(testo_mail, 'html')
                        m['Subject'] = 'Resoconto ore lavorate nel mese %s' % nome
                        m['From'] = settings.EMAIL_HOST_USER
                        m['To'] = mail + "," + settings.EMAIL_HOST_USER
                        mail_sending(m)
                        print(r.reminder_mail)
                        r.reminder_boolean = True
                        r.save()'''
            u.save()



