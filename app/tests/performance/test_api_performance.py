import unittest
import requests
import time

class TestAPIPerformance(unittest.TestCase):
    base_url = "http://127.0.0.1:5000/api/accounts"
    timeout = 0.5

    def setUp(self):
        for i in range(100):
            pesel = f"1234567{i:03d}"
            try:
                requests.delete(f"{self.base_url}/{pesel}", timeout=self.timeout)
            except requests.exceptions.RequestException:
                pass

    def test_create_delete_100_accounts(self):
        for i in range(100):
            test_data = {
                "imie": f"Test{i}",
                "nazwisko": f"User{i}",
                "pesel": f"1234567{i:03d}"
            }
            
            start_time = time.time()
            create_response = requests.post(self.base_url, json=test_data, timeout=self.timeout)
            response_time = time.time() - start_time
            
            if create_response.status_code != 201:
                self.fail(f"Failed to create account {i}. Status: {create_response.status_code}")
            self.assertLess(response_time, 0.5, f"Account creation took too long: {response_time}s")
            
            start_time = time.time()
            delete_response = requests.delete(f"{self.base_url}/{test_data['pesel']}", timeout=self.timeout)
            response_time = time.time() - start_time
            
            self.assertIn(delete_response.status_code, [200, 404], f"Unexpected status code when deleting account {i}")
            self.assertLess(response_time, 0.5, f"Account deletion took too long: {response_time}s")

    def test_100_transfers(self):
        account1_data = {
            "imie": "Account",
            "nazwisko": "One",
            "pesel": "12345678901",
            "promo": "PROM_XYZ"
        }
        account2_data = {
            "imie": "Account",
            "nazwisko": "Two",
            "pesel": "98765432109",
            "promo": "PROM_XYZ"
        }

        response = requests.post(self.base_url, json=account1_data, timeout=self.timeout)
        self.assertEqual(response.status_code, 201, "Failed to create first account")
        
        response = requests.post(self.base_url, json=account2_data, timeout=self.timeout)
        self.assertEqual(response.status_code, 201, "Failed to create second account")

        transfer_amount = 1

        for i in range(100):
            sender = account1_data["pesel"] if i % 2 == 0 else account2_data["pesel"]
            receiver = account2_data["pesel"] if i % 2 == 0 else account1_data["pesel"]

            transfer_data = {
                "receiver": receiver,
                "amount": transfer_amount,
                "type": "normal"
            }
            
            start_time = time.time()
            response = requests.post(f"{self.base_url}/{sender}/transfer", json=transfer_data, timeout=self.timeout)
            response_time = time.time() - start_time
            
            self.assertEqual(response.status_code, 200, f"Transfer {i} failed. Sender: {sender}, Receiver: {receiver}")
            self.assertLess(response_time, 0.5, f"Transfer {i} took too long: {response_time}s")

        response1 = requests.get(f"{self.base_url}/{account1_data['pesel']}", timeout=self.timeout)
        response2 = requests.get(f"{self.base_url}/{account2_data['pesel']}", timeout=self.timeout)
        
        balance1 = response1.json()["saldo"]
        balance2 = response2.json()["saldo"]
        
        self.assertEqual(balance1 + balance2, 100, f"Total balance incorrect. Account1: {balance1}, Account2: {balance2}")

    def tearDown(self):
        try:
            requests.delete(f"{self.base_url}/12345678901", timeout=self.timeout)
            requests.delete(f"{self.base_url}/98765432109", timeout=self.timeout)
        except requests.exceptions.RequestException:
            pass

if __name__ == '__main__':
    unittest.main()