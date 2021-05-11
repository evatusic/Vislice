import json
import random

STEVILO_DOVOLJENIH_NAPAK = 9
PRAVILNA_CRKA, PONOVLJENA_CRKA, NAPACNA_CRKA = '+', 'o', '-'
ZMAGA, PORAZ = 'w', 'x'
ZACETEK = 's'

DATOTEKA_S_STANJEM = "stanje.json"
DATOTEKA_Z_BESEDAMI = "besede.txt"

class Vislice:
    def __init__(self, datoteka_s_stanjem):
        self.igre = {}
        self.max_id = 0
        self.datoteka_s_stanjem = datoteka_s_stanjem
        
        

    def prost_id_igre(self):
        self.max_id += 1
        return self.max_id

   # def prost_id_igre_drugace(self):  DRUGA MOZNOST
   # if not self.igre: return 0
    #    m = max(self.igre.keys())
    #    return m + 1

    def nova_igra(self):
        self.nalozi_igre_iz_datoteke()
        nov_id = self.prost_id_igre()
        sveza_igra = nova_igra()
        self.igre[nov_id] = (sveza_igra, ZACETEK)
        self.zapisi_igre_v_datoteko()
        return nov_id

    def ugibaj(self, id_igre, crka):
        self.nalozi_igre_iz_datoteke()
        igra, _ = self.igre[id_igre]
        novo_stanje = igra.ugibaj(crka)
        self.igre[id_igre] = (igra, novo_stanje)
        self.zapisi_igre_v_datoteko()
          

    def nalozi_igre_iz_datoteke(self):
        with open(self.datoteka_s_stanjem, encoding='utf-8') as f:
            igre = json.load(f)
            self.igre = {int(id_igre): (Igra(geslo, crka), stanje) for id_igre, (geslo, crka, stanje) in igre.items()}

    def zapisi_igre_v_datoteko(self):
        with open(self.datoteka_s_stanjem, 'w', encoding='utf-8') as f:
            igre = {id_igre: (igra.geslo, igra.crke, stanje) for id_igre, (igra, stanje) in self.igre.items()}
            json.dump(igre, f)

class Igra:
    def __init__(self, geslo, crke=None):
        self.geslo = geslo
        if crke is None:
            self.crke = []
        else:
            self.crke = crke

    def napacne_crke(self):
        return [c for c in self.crke if c.upper() not in self.geslo.upper()]
        
    def pravilne_crke(self):
        return [c for c in self.crke if c.upper() in self.geslo.upper()]

    def stevilo_napak(self):
        return len(self.napacne_crke())

    def poraz(self):
        return self.stevilo_napak() > STEVILO_DOVOLJENIH_NAPAK

    def zmaga(self):
        return not self.poraz() and len(set(self.pravilne_crke())) == len(set(self.geslo))

    def pravilni_del_gesla(self):
        pravilno = ''
        for c in self.geslo.upper():
            if c in self.crke:
                pravilno += c + ' '
            else:
                pravilno += '_ '
        return pravilno

        #return''.join([c if c in self.crke esle '_' for c in self.geslo.upper()])
    def nepravilni_ugibi(self):
        return ' '.join(self.napacne_crke())
    
    def ugibaj(self, crka):
        crka = crka.upper()
        if crka in self.crke:
            return PONOVLJENA_CRKA
        elif crka in self.geslo.upper():
            self.crke.append(crka)
            if self.zmaga():
                return ZMAGA
            else:
                return PRAVILNA_CRKA
        else:
            self.crke.append(crka)
            if self.poraz():
                return PORAZ
            else:
                return NAPACNA_CRKA
    
with open(DATOTEKA_Z_BESEDAMI, encoding="utf-8") as f:
    bazen_besed = f.read().split()



def nova_igra():
    geslo = random.choice(bazen_besed)
    return Igra(geslo)

    


    
    
            



        





