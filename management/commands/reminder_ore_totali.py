class Command(BaseCommand):
    help = 'Promemoria scadenza dominio'

    def mail_sending(m):
        s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        s.starttls()
        s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        s.send_message(m)
        s.quit()

    def handle(self, *args, **options):
        today = datetime.date.today()

        expire_day = today + datetime.timedelta(days=6)
        reminder = Reminder.objects.filter(reminder_date__gte=today, reminder_date__lte=expire_day,reminder_boolean = False)
        for r in reminder:
            nome = r.reminder_name
            mail = r.reminder_mail
            dominio = r.reminder_domain
            testo_mail = "Buonasera %s,<br><br>" "Il tuo abbonamento al dominio %s sta per scadere" % (nome, dominio)
            m = MIMEText(testo_mail, 'html')
            m['Subject'] = 'Promemoria scadenza Dominio %s' % nome
            m['From'] = settings.EMAIL_HOST_USER
            m['To'] = mail + "," + settings.EMAIL_HOST_USER
            mail_sending(m)
            print (r.reminder_mail)
            r.reminder_boolean=True
            r.save()