import unittest
from app.Konto_firmowe import *
from parameterized import parameterized
from unittest.mock import patch, MagicMock


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

    @patch('app.Konto_firmowe.Konto_firmowe.checkNIP', return_value=True)
    def test_checkNIP_valid(self, mock_checkNIP):
        konto = Konto_firmowe(nazwa=self.nazwa, NIP=self.NIP)
        self.assertEqual(konto.nazwa, self.nazwa, "Nie zapisano nazwy!")
        self.assertEqual(konto.NIP, self.NIP, "Nie zapisano NIPu!")
        self.assertEqual(konto.saldo, 0, "Niepoprawny stan konta!")
        mock_checkNIP.assert_called_once()

    @patch('app.Konto_firmowe.Konto_firmowe.checkNIP', return_value=False)
    def test_checkNIP_invalid_raises_error(self, mock_checkNIP):
        with self.assertRaises(ValueError) as context:
            Konto_firmowe(nazwa=self.nazwa, NIP=self.NIP)
        self.assertEqual(str(context.exception), "Company not registered!!")
        mock_checkNIP.assert_called_once()

    @parameterized.expand([
        ("NIP za krótki", "1234", "Niepoprawny NIP!"),
        ("NIP za długi", "12345678901234", "Niepoprawny NIP!"),
    ])
    def test_NIP_validation(self, name, test_NIP, expected):
        konto = Konto_firmowe(nazwa=self.nazwa, NIP=test_NIP)
        self.assertEqual(konto.NIP, expected, f"{name}: Walidacja NIP nie działa poprawnie!")

    @patch('app.Konto_firmowe.Konto_firmowe.checkNIP', return_value=False)
    def test_constructor_unregistered_company(self, mock_checkNIP):
        with self.assertRaises(ValueError) as context:
            Konto_firmowe(nazwa=self.nazwa, NIP=self.NIP)
        self.assertEqual(str(context.exception), "Company not registered!!")
        mock_checkNIP.assert_called_once()

    @patch('app.Konto_firmowe.Konto_firmowe.checkNIP', return_value=True)
    def test_constructor_valid_company(self, mock_checkNIP):
        konto = Konto_firmowe(nazwa=self.nazwa, NIP=self.NIP)
        self.assertIsInstance(konto, Konto_firmowe)
        mock_checkNIP.assert_called_once()

    @patch('app.Konto_firmowe.req.get')
    def test_checkNIP_fails(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        konto = Konto_firmowe.__new__(Konto_firmowe)
        konto.nazwa = "Test Firma"
        konto.NIP = "1234567890"
        self.assertFalse(konto.checkNIP(), "checkNIP should return False for non-200 responses.")
