import unittest

from ..Konto import *
from parameterized import *

class TestCreateBankAccount(unittest.TestCase):
    def setUp(self): 
        self.imie = "Dariusz"
        self.nazwisko = "Januszewski"
        self.pesel = "12345678900"
        self.promo = "PROM_XYZ"
        self.senior_pesel = "65010112345"

    def test_tworzenie_konta(self):
        pierwsze_konto = Konto_osobiste(self.imie, self.nazwisko, self.pesel)
        self.assertEqual(pierwsze_konto.imie, self.imie, "Imie nie zostało zapisane!")
        self.assertEqual(pierwsze_konto.nazwisko, self.nazwisko, "Nazwisko nie zostało zapisane!")
        self.assertEqual(pierwsze_konto.saldo, 0, "Saldo nie jest zerowe!")
        self.assertEqual(pierwsze_konto.historia, [], "Historia nie jest pusta!")

    #tutaj proszę dodawać nowe testy

    @parameterized.expand([
        ("test_krotki_pesel", "Pesel nie został zapisany - za krótki", "1234", "Niepoprawny pesel!"),
        ("test_dlugi_pesel", "Pesel nie został zapisany - za długi", "12345678901234", "Niepoprawny pesel!")

    ])
    def test_pesel(self, name, error, test_pesel, result):
        print(f"Test: {name}")
        konto = Konto_osobiste(self.imie, self.nazwisko, test_pesel)
        self.assertEqual(konto.pesel, result, f"Error: {error}")

    @parameterized.expand([
        ("test_zly_kod", "Kod jest niepoprawny", "PROM_12345", 0),
        ("test_poprawny_kod", "Kod jest poprawny ale nie przypisano srodkow", "PROM_XYZ", 50),
        ("test_brak_kodu", "Przypisano środki bez kodu!", "", 0),
        ("test_promo_senior", "Przypisano środki z kodu seniorowi!", "PROM_XYZ", 0, "senior")

    ])
    def test_promo_kod(self, name, error, test_promo, result, pesel_type = ""):
        print(f"Test: {name}")
        pesel = self.senior_pesel if pesel_type == "senior" else self.pesel
        konto = Konto_osobiste(self.imie, self.nazwisko, pesel, promo = test_promo)
        self.assertEqual(konto.saldo, result, f"Error: {error}")
