class Konto:
    def __init__(self):
        self.saldo = 0
        self.oplata_ekspres = 0

    def przelew(self, adresat, kwota):
        if(self.saldo > kwota):
            self.saldo -= kwota
            adresat.saldo += kwota

    def ekspres(self, adresat, kwota):
        if(self.saldo > kwota - self.oplata_ekspres):
            self.saldo = self.saldo - kwota - self.oplata_ekspres
            adresat.saldo += kwota


class Konto_osobiste(Konto):
    def __init__(self, imie, nazwisko, pesel, promo = ""):
        super().__init__()
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.promo = promo
        self.oplata_ekspres = 1
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

class Konto_firmowe(Konto):
    def __init__(self, nazwa, NIP):
        super().__init__()
        self.nazwa = nazwa
        self.NIP = NIP
        self.oplata_ekspres = 5
        self.test_NIP()

    def test_NIP(self):
        if len(self.NIP) != 10:
            self.NIP = "Niepoprawny NIP!"
