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

    def test_przelew_zaksiegowanie(self):
        self.konto_1.saldo = 200
        self.konto_2.saldo = 0
        self.konto_1.historia = []
        self.konto_2.historia = []
        self.konto_1.przelew(self.konto_2, self.kwota_przelewu)
        self.assertEqual(self.konto_1.historia, [-50], "Nie zaksiegowano poprawnie przelewu")
        self.assertEqual(self.konto_2.historia, [50], "Nie zaksiegowano poprawnie przelewu")

    @parameterized.expand([
        ("test_ekspres_osobiste", "osobiste", "Nie zaksiegowano przelewu ekspresowego osobistego", [-50, -1]),
        ("test_ekspres_firmowe", "firmowe", "Nie zaksiegowano przelewu ekspresowego firmowego", [-50, -5])

    ])
    def test_ekspres_zaksiegowanie(self, name, sender_type, error, result):
        print(f"Test: {name}")
        sender = self.konto_1 if sender_type == "osobiste" else self.konto_firm
        sender.saldo = self.base_saldo
        self.konto_2.saldo = 0
        sender.historia = []
        self.konto_2.historia = []
        sender.ekspres(self.konto_2, self.kwota_przelewu)
        self.assertEqual(sender.historia, result, f"Error: {error}")
        self.assertEqual(self.konto_2.historia, [50], "Nie zaksiegowano poprawnie przelewu")
