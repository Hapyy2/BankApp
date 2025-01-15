import unittest
from unittest.mock import patch
from datetime import datetime
from app.Konto_osobiste import Konto_osobiste
from app.Konto_firmowe import Konto_firmowe

class TestSendHistoryToEmail(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Januszewski"
    pesel = "12345678900"
    expected_history = [123, 432, -123, 541, -100, 235]
    email = "januszewski@mail.com"
    expected_email_subject = "Wyciąg z dnia " + datetime.now().strftime('%Y-%m-%d')
    text_os = "Twoja historia konta to: " + str(expected_history)
    text_firm = "Historia konta Twojej firmy to: " + str(expected_history)

    def setUp(self):
        self.konto = Konto_osobiste(self.imie, self.nazwisko, self.pesel)
        self.konto.historia = self.expected_history
        self.konto_firmowe = Konto_firmowe("Adamex", "1234567890")
        self.konto_firmowe.historia = self.expected_history
    
    @patch("app.Konto.SMTPClient")
    def test_send_history_to_email_osobiste_success(self, send_mock):
        smtp_instance = send_mock.return_value
        smtp_instance.send.return_value = True
        result = self.konto.send_history_to_email(self.email, smtp_instance)
        self.assertTrue(result)
        smtp_instance.send.assert_called_once_with(
            self.expected_email_subject,
            self.text_os,
            self.email,
        )

    @patch("app.Konto.SMTPClient")
    def test_send_history_to_email_osobiste_failure(self, send_mock):
        smtp_instance = send_mock.return_value
        smtp_instance.send.return_value = False
        result = self.konto.send_history_to_email(self.email, smtp_instance)
        self.assertFalse(result)
        smtp_instance.send.assert_called_once_with(
            self.expected_email_subject,
            self.text_os,
            self.email,
        )

    @patch("app.Konto.SMTPClient")
    def test_send_history_to_email_firmowe_success(self, send_mock):
        smtp_instance = send_mock.return_value
        smtp_instance.send.return_value = True
        result = self.konto_firmowe.send_history_to_email(self.email, smtp_instance)
        self.assertTrue(result)
        smtp_instance.send.assert_called_once_with(
            self.expected_email_subject,
            self.text_firm,
            self.email,
        )

    @patch("app.Konto.SMTPClient")
    def test_send_history_to_email_firmowe_failure(self, send_mock):
        smtp_instance = send_mock.return_value
        smtp_instance.send.return_value = False
        result = self.konto_firmowe.send_history_to_email(self.email, smtp_instance)
        self.assertFalse(result)
        smtp_instance.send.assert_called_once_with(
            self.expected_email_subject,
            self.text_firm,
            self.email,
        )

