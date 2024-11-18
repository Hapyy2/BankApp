import unittest

from app.Accounts_Registry import *
from app.Konto_osobiste import *
from parameterized import *

class TestRegistry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.konto_os = Konto_osobiste("Jan", "Kowalski", "12345678901")

    def setUp(self):
        Accounts_Registry.registry = []
    
    def test_add_acc(self):
        Accounts_Registry.AddAccount(self.konto_os)
        self.assertEqual(Accounts_Registry.registry[-1], self.konto_os, "Nie dodano konta do rejestru")

    def test_search_acc_found(self):
        Accounts_Registry.AddAccount(self.konto_os)
        searched = Accounts_Registry.SearchAccount("11122233344")
        self.assertEqual(searched, "Nie znaleziono konta z podanym peselem", f"Error: Błąd")
    
    def test_search_acc_not_found(self):
        Accounts_Registry.AddAccount(self.konto_os)
        searched = Accounts_Registry.SearchAccount("12345678901")
        self.assertEqual(searched, self.konto_os, f"Error: Nie znaleziono konta z podanym peselem a powinno")

    def test_count_acc(self):
        Accounts_Registry.AddAccount(self.konto_os)
        count = Accounts_Registry.CountAccount()
        self.assertEqual(count, 1, "Nieprawidłowo policzono ilość kont")