import unittest

from app.Konto_firmowe import *
from parameterized import *

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

    @patch('app.Konto_firmowe.req.get')
    def test_checkNIP_valid(self, mock_get):
        # Mockowanie odpowiedzi requestu
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        konto = Konto_firmowe(nazwa="Test Firma", NIP="1234567890")
        self.assertTrue(konto.checkNIP())

    @patch('app.Konto_firmowe.req.get')
    def test_checkNIP_invalid(self, mock_get):
        # Mockowanie odpowiedzi requestu
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            Konto_firmowe(nazwa="Test Firma", NIP="1234567890")
        
        # Opcjonalne: możesz sprawdzić wiadomość wyjątku
        self.assertEqual(str(context.exception), "Company not registered!!")


    def test_invalid_NIP_length(self):
        # NIP krótszy niż 10 znaków
        konto = Konto_firmowe(nazwa="Test Firma", NIP="12345")
        self.assertEqual(konto.NIP, "Niepoprawny NIP!")

    @patch('app.Konto_firmowe.req.get')
    def test_constructor_raises_error_for_unregistered_company(self, mock_get):
        # Mockowanie requestu jako nieistniejąca firma
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            Konto_firmowe(nazwa="Test Firma", NIP="1234567890")
        self.assertEqual(str(context.exception), "Company not registered!!")

    @patch('app.Konto_firmowe.req.get')
    def test_constructor_does_not_raise_error_for_valid_company(self, mock_get):
        # Mockowanie requestu jako poprawna firma
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        konto = Konto_firmowe(nazwa="Test Firma", NIP="1234567890")
        self.assertIsInstance(konto, Konto_firmowe)
