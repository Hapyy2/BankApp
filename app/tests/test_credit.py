import unittest

from ..Konto import *
from parameterized import *

class TestCredit(unittest.TestCase):
    def setUp(self):
        self.konto_os = Konto_osobiste("Jan", "Kowalski", "20210112345")
        self.konto_firm = Konto_firmowe("Adamex", "1234567890")
        self.kwota = 500
    
    @parameterized.expand([
        ("warunek_1", "Nie udzielono kredytu! - warunek 1 spełniony", [-5, 50, 50, 50], 500),
        ("warunek_2", "Nie udzielono kredytu! - warunek 2 spełniony", [-10000, 250, 250, 50, 50, -50], 500),
        ("nie_udzielenie_kredytu", "Udzielono kredytu! - oba warunki nie spełnione", [-5, 50, -50, 50, 50], 0)

    ])
    def test_udzielenie_kredytu_osobistego(self, name, error, test_history, result):
        print(f"Test: {name}")
        self.konto_os.historia = test_history
        self.konto_os.saldo = 0
        self.konto_os.zaciagnij_kredyt(self.kwota) 
        self.assertEqual(self.konto_os.saldo, result, f"Error: {error}")

    @parameterized.expand([
        ("warunek_1", "Udzielono kredytu! - tylko warunek 1 spełniony", [-5, 50, 50], 1000, 1000),
        ("warunek_2", "Udzielono kredytu! - tylko warunek 2 spełniony", [-500, 1775, 32, 123], 0, 0),
        ("nie_udzielenie_kredytu", "Udzielono kredytu! - oba warunki nie spełnione", [-5, 50, 50], 0, 0),
        ("udzielenie_kredytu", "Nie udzielono kredytu! - oba warunki spełnione", [-5, 1775, 50, 50], 1000, 1500)

    ])
    def test_udzielenie_kredytu_firmowego(self, name, error, test_history, test_saldo, result):
        print(f"Test: {name}")
        self.konto_firm.historia = test_history
        self.konto_firm.saldo = test_saldo
        self.konto_firm.zaciagnij_kredyt(self.kwota)
        self.assertEqual(self.konto_firm.saldo, result, f"Error: {error}")
