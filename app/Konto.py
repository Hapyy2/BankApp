class Konto:
    def __init__(self, imie, nazwisko, pesel, promo = ""):
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.saldo = 0
        self.promo = promo
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
