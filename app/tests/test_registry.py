import unittest

from app.Accounts_Registry import *
from app.Konto_osobiste import *
from parameterized import *

class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.konto_os = Konto_osobiste("Jan", "Kowalski", "12345678901")
        self.test_reg = Accounts_Registry()
    
    def test_add_acc(self):
        self.test_reg.AddAccount(self.konto_os)
        self.assertEqual(self.test_reg.registry[-1], self.konto_os, "Nie dodano konta do rejestru")

    # @parameterized.expand([
    #     ("test_znaleziono", "Błąd", "11122233344", "Nie znaleziono konta z podanym peselem"),
    #     ("test_nie_znaleziono", "Nie znaleziono konta z podanym peselem a powinno", "12345678901", self.konto_os)

    # ])
    # def test_search_acc(self, name, error, test_pesel, result):
    #     print(f"Test: {name}")

    #     self.test_reg.AddAccount(self.konto_os)
    #     searched = self.test_reg.SearchAccount(test_pesel)

    #     self.assertEqual(searched, result, f"Error: {error}")

    def test_search_acc_found(self):
        self.test_reg.AddAccount(self.konto_os)
        searched = self.test_reg.SearchAccount("11122233344")
        self.assertEqual(searched, "Nie znaleziono konta z podanym peselem", f"Error: Błąd")
    
    def test_search_acc_not_found(self):
        self.test_reg.AddAccount(self.konto_os)
        searched = self.test_reg.SearchAccount("12345678901")
        self.assertEqual(searched, self.konto_os, f"Error: Nie znaleziono konta z podanym peselem a powinno")

    def test_count_acc(self):
        self.test_reg.AddAccount(self.konto_os)
        count = self.test_reg.CountAccount()
        self.assertEqual(count, 1, "Nieprawidłowo policzono ilość kont")