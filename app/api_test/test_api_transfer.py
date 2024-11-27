import unittest
import requests as req

class TestAPITransfer(unittest.TestCase):
    base_url = "http://127.0.0.1:5000/api/accounts"
    person1 = {
        "imie": "Jan",
        "nazwisko": "Kowalski",
        "pesel": "12345678901",
        "promo": "PROM_XYZ"
    }
    person2 = {
        "imie": "Adam",
        "nazwisko": "Nowak",
        "pesel": "12349999999"
    }
    base_body = {
        "amount": "47",
        "type": "normal",
        "receiver": "12349999999"
    }
    invalid_pesel = "99999999999"

    def setUp(self):
        req.post(self.base_url, json=self.person1)
        req.post(self.base_url, json=self.person2)

    def tearDown(self):
        req.delete(f'{self.base_url}/{self.person1["pesel"]}')
        req.delete(f'{self.base_url}/{self.person2["pesel"]}')
    
    def test_no_sender(self):
        response = req.post(f'{self.base_url}/{self.invalid_pesel}/transfer', json=self.base_body)
        self.assertEqual(response.status_code, 404, "Wrong status code - sender does not exist")
    
    def test_correct_normal(self):
        response = req.post(f'{self.base_url}/{self.person1["pesel"]}/transfer', json=self.base_body)
        self.assertEqual(response.status_code, 200, "Wrong status code - properly sent normal transfer request")
    
    def test_no_receiver(self):
        body = self.base_body
        body["receiver"] = self.invalid_pesel
        response = req.post(f'{self.base_url}/{self.person1["pesel"]}/transfer', json=body)
        self.assertEqual(response.status_code, 404, "Wrong status code - receiver does not exist")

    def test_correct_ekspres(self):
        body = self.base_body
        body["type"] = "express"
        response = req.post(f'{self.base_url}/{self.person1["pesel"]}/transfer', json=body)
        self.assertEqual(response.status_code, 200, "Wrong status code - properly sent express transfer request")
    
    def test_unknown_type(self):
        body = self.base_body
        body["type"] = "unknown"
        response = req.post(f'{self.base_url}/{self.person1["pesel"]}/transfer', json=body)
        self.assertEqual(response.status_code, 404, "Wrong status code - unknown transfer type")
    
    def test_insufficient_funds(self):
        body = self.base_body
        body["amount"] = "1000"
        response = req.post(f'{self.base_url}/{self.person1["pesel"]}/transfer', json=body)
        self.assertEqual(response.status_code, 422, "Wrong status code - insufficient funds")
