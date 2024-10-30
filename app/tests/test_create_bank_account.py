import unittest

from ..Konto import Konto

class TestCreateBankAccount(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Januszewski"
    pesel = "12345678900"
    promo = "PROM_XYZ"

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
    
    def test_brak_kodu(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        self.assertEqual(konto.saldo, 0, "Przypisano środki bez kodu!")
    
    def test_promo_senior(self):
        senior_pesel = "65010112345"
        konto = Konto(self.imie, self.nazwisko, senior_pesel, self.promo)
        self.assertEqual(konto.saldo, 0, "Przypisano środki z kodu seniorowi!")

class TestTransfer(unittest.TestCase):
    konto_1 = Konto("Jan", "Kowalski", "20210112345")
    konto_2 = Konto("Anna", "Nowak", "12345678901")
    kwota_przelewu = 50

    def test_przelew_wysylajacy(self):
        self.konto_1.saldo = 200
        self.konto_2.saldo = 0
        self.konto_1.przelew(self.konto_2, self.kwota_przelewu)
        self.assertEqual(self.konto_1.saldo, 150, "Nie odjeło środków")
    
    def test_przelew_adresat(self):
        self.konto_1.saldo = 200
        self.konto_2.saldo = 0
        self.konto_1.przelew(self.konto_2, self.kwota_przelewu)
        self.assertEqual(self.konto_2.saldo, 50, "Nie przekazano środków")
        
    def test_saldo_na_minus(self):
        self.konto_1.saldo = 200
        self.konto_2.saldo = 0
        self.konto_2.przelew(self.konto_1, self.kwota_przelewu)
        self.assertEqual(self.konto_2.saldo, 0, "Nie można przelać niedostępnych środków")
    
    