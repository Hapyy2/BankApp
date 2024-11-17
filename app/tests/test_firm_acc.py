import unittest

from app.Konto_firmowe import *
from parameterized import *

class TestFirmAccount(unittest.TestCase):
    def setUp(self):
        self.nazwa = "Adamex"
        self.NIP = "1234567890"

    def test_tworzenie_konta(self):
        konto_firm = Konto_firmowe("Adamex", "1234567890")
        self.assertEqual(konto_firm.nazwa, self.nazwa, "Nazwa nie została zapisane!")
        self.assertEqual(konto_firm.NIP, self.NIP, "NIP nie został zapisane!")
        self.assertEqual(konto_firm.saldo, 0, "Saldo nie jest zerowe!")

    @parameterized.expand([
        ("test_krotki_NIP", "NIP nie został zapisany - za krótki", "1234", "Niepoprawny NIP!"),
        ("test_dlugi_NIP", "NIP nie został zapisany - za długi", "12345678901234", "Niepoprawny NIP!")

    ])
    def test_NIP(self, name, error, test_NIP, result):
        print(f"Test: {name}")
        konto_firm = Konto_firmowe(self.nazwa, test_NIP)
        self.assertEqual(konto_firm.NIP, result, f"Error: {error}")
