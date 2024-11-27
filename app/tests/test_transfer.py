import unittest

from app.Konto_osobiste import *
from app.Konto_firmowe import *
from parameterized import *

class TestTransfer(unittest.TestCase):
    def setUp(self): 
        self.konto_1 = Konto_osobiste("Jan", "Kowalski", "20210112345")
        self.konto_2 = Konto_osobiste("Anna", "Nowak", "12345678901")
        self.konto_firm = Konto_firmowe("Adamex", "1234567890")
        self.kwota_przelewu = 50
        self.base_saldo = 200

    @parameterized.expand([
        ("test_przelew_wysylajacy", "Nie odjeło środków", 200, 150, True),
        ("test_saldo_na_minus", "Nie można przelać niedostępnych środków", 0, 0, False)

    ])
    def test_przelew_wychodzacy(self, name, error, base_saldo, result, expected_return):
        print(f"Test: {name}")
        self.konto_1.saldo = base_saldo
        flag = self.konto_1.przelew(self.konto_2, self.kwota_przelewu)
        self.assertEqual(self.konto_1.saldo, result, f"Error: {error}")
        self.assertEqual(flag, expected_return, f"Error: Zwrócono niepoprawny status")

    def test_przelew_dostarczenie_srodkow(self):
        self.konto_1.saldo = 200
        self.konto_2.saldo = 0
        flag = self.konto_1.przelew(self.konto_2, self.kwota_przelewu)
        self.assertEqual(self.konto_2.saldo, 50, "Nie przekazano środków")
        self.assertEqual(flag, True, "Zwrócono niepoprawny status")
  
    @parameterized.expand([
        ("osobiste", "osobiste", "Nie odjeło środków", 200, 149, True),
        ("saldo_na_minus", "osobiste", "Nie można przelać niedostępnych środków", 0, 0, False),
        ("firmowe", "firmowe", "Nie odjeło środków", 200, 145, True)

    ])
    def test_ekspres(self, name, sender_type, error, base_saldo, result, expected_return):
        print(f"Test: {name}")
        sender = self.konto_1 if sender_type == "osobiste" else self.konto_firm
        sender.saldo = base_saldo
        sender.ekspres(self.konto_2, self.kwota_przelewu)
        self.assertEqual(sender.saldo, result, f"Error: {error}")

    def test_ekspres_dostarczenie_srodkow(self):
        self.konto_1.saldo = 200
        self.konto_2.saldo = 0
        flag = self.konto_1.ekspres(self.konto_2, self.kwota_przelewu)
        self.assertEqual(self.konto_2.saldo, 50, "Nie przekazano środków")
        self.assertEqual(flag, True, "Zwrócono niepoprawny status")
