from app.Konto import *

class Konto_osobiste(Konto):
    def __init__(self, imie, nazwisko, pesel, promo = ""):
        super().__init__()
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.promo = promo
        self.oplata_ekspres = 1
        self.history_message = "Twoja historia konta to"
        self.test_pesel()
        self.test_kodu(promo)

    def test_pesel(self):
        if len(self.pesel) != 11:
            self.pesel = "Niepoprawny pesel!"

    def test_kodu(self, kod):
        if kod[0:5] == "PROM_" and len(kod) == 8 and self.test_senior() == False:
            self.saldo = 50

    def test_senior(self):
        rok = int(self.pesel[:2])
        miesiac = int(self.pesel[2:4])
        return (rok > 60 and miesiac <= 12) or (miesiac >= 21 and miesiac <= 32)
    
    def zaciagnij_kredyt(self, kwota):
        if self.war_kredyt_1() or self.war_kredyt_2(kwota):
            self.saldo += kwota
            self.historia.append(kwota)
    
    def war_kredyt_1(self):
        i = -3
        while i < 0:
            if self.historia[i] < 0:
                return False
            i += 1
        return True

    def war_kredyt_2(self, kwota):
        return len(self.historia) >= 5 and sum(self.historia[-5:]) > kwota
