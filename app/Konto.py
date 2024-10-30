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
        if kod[0:5] == "PROM_" and len(kod) == 8:
            self.saldo = 50
