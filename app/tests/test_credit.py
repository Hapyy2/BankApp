import unittest

from ..Konto import *
from parameterized import *

class TestCredit(unittest.TestCase):
    def setUp(self):
        self.konto = Konto_osobiste("Jan", "Kowalski", "20210112345")
        self.kwota = 500
    
    @parameterized.expand([
        ("warunek_1", "Nie udzielono kredytu! - warunek 1 spełniony", [-5, 50, 50, 50], 500),
        ("warunek_2", "Nie udzielono kredytu! - warunek 2 spełniony", [-10000, 250, 250, 50, 50, -50], 500),
        ("nie_udzielenie_kredytu", "Udzielono kredytu! - oba warunki nie spełnione", [-5, 50, -50, 50, 50], 0)

    ])
    def test_udzielenie_kredytu(self, name, error, test_history, result):
        print(f"Test: {name}")
        self.konto.historia = test_history
        self.konto.saldo = 0
        self.konto.zaciagnij_kredyt(self.kwota)
        self.assertEqual(self.konto.saldo, result, f"Error: {error}")
