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
        Accounts_Registry.AddAccount(self.konto_os)
    
    def test_add_acc(self):
        self.assertEqual(Accounts_Registry.registry[-1], self.konto_os, "Nie dodano konta do rejestru")

    def test_search_acc_found(self):
        searched = Accounts_Registry.SearchAccount("12345678901")
        self.assertEqual(searched, self.konto_os, f"Error: Nie znaleziono konta z podanym peselem a powinno")

    def test_search_acc_not_found(self):
        searched = Accounts_Registry.SearchAccount("11122233344")
        self.assertEqual(searched, False, f"Error: Błąd")

    def test_count_acc(self):
        count = Accounts_Registry.CountAccount()
        self.assertEqual(count, 1, "Nieprawidłowo policzono ilość kont")

    @parameterized.expand([
        ("12345678901", {"imie": "Kowal"}, "imie", "Kowal", "Nie zaktualizowano imienia"),
        ("12345678901", {"nazwisko": "Pomorski"}, "nazwisko", "Pomorski", "Nie zaktualizowano nazwiska"),
        ("12345678901", {"pesel": "10987654321"}, "pesel", "10987654321", "Nie zaktualizowano peselu")

    ])
    def test_update_acc(self, test_pesel, test_data, tested, expected, error):
        Accounts_Registry.UpdateAccount(test_pesel, test_data)
        result = Accounts_Registry.registry[0]
        self.assertEqual(getattr(result, tested) , expected, f"Error: {error}")
    
    def test_update_acc_fail(self):
        Accounts_Registry.UpdateAccount("11111111111", {})
        result = Accounts_Registry.UpdateAccount("11111111111", {})
        self.assertEqual(result , False, f"Error: Coś poszło nie tak")
    
    @parameterized.expand([
        ("12345678901", 0, "Nie usunięto konta"),
        ("11111111111", 1, "Usunięto konto z nieprawidłowym peselem")

    ])
    def test_delete_acc(self, test_pesel, expected, error):
        Accounts_Registry.DeleteAccount(test_pesel)
        self.assertEqual(len(Accounts_Registry.registry), expected, f"Error: {error}")