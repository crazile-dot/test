from APIauth.models import User

def handle(self, *args, **options):
    max = 0
    conf = 0
    ing_name = ""
    name = ""
    for u in User.objects.all():
        ore_mensili = int(u.fascia_oraria_mensile)*4
        if int(u.ore_mese_attuale_lavorate) > ore_mensili:
            conf = int(u.ore_mese_attuale_lavorate) - ore_mensili
            name = u.email
            if conf > max:
                max = conf
                ing_name = name

    ing_mese = ing_name
    ore_ing_mese = max

    for u in User.objects.all():
        if ing_mese == u.email:
            u.ing_mese = True
        else:
            u.ing_mese = False

    #possiamo mostrare da frontend il nome
    #dell'ingegnere del mese in una sezione dedicata
    #in più manderemo una mail al vincitore
