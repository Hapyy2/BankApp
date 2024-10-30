import unittest

from ..Konto import Konto

class TestCreateBankAccount(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Januszewski"
    pesel = "12345678900"

    def test_tworzenie_konta(self):
        pierwsze_konto = Konto(self.imie, self.nazwisko, self.pesel)
        self.assertEqual(pierwsze_konto.imie, self.imie, "Imie nie zostało zapisane!")
        self.assertEqual(pierwsze_konto.nazwisko, self.nazwisko, "Nazwisko nie zostało zapisane!")
        self.assertEqual(pierwsze_konto.saldo, 0, "Saldo nie jest zerowe!")

    #tutaj proszę dodawać nowe testy

    def test_krotki_pesel(self):
        zly_pesel = "1234"
        konto = Konto(self.imie, self.nazwisko, zly_pesel)
        self.assertEqual(konto.pesel, "Niepoprawny pesel!", "Pesel nie został zapisany - za krótki")
    
    def test_dlugi_pesel(self):
        zly_pesel = "12345678901234"
        konto = Konto(self.imie, self.nazwisko, zly_pesel)
        self.assertEqual(konto.pesel, "Niepoprawny pesel!", "Pesel nie został zapisany - za długi")

    def test_zly_kod(self):
        kod = "PROM_12345"
        konto = Konto(self.imie, self.nazwisko, self.pesel, promo = kod)
        self.assertEqual(konto.saldo, 0, "Kod jest niepoprawny")
    
    def test_poprawny_kod(self):
        kod = "PROM_XYZ"
        konto = Konto(self.imie, self.nazwisko, self.pesel, promo = kod)
        self.assertEqual(konto.saldo, 50, "Kod jest poprawny ale nie przypisano srodkow")
    
    def brak_kodu(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        self.assertEqual(konto.saldo, 0, "Przypisano środki bez kodu!")