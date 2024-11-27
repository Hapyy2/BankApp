import unittest
import requests as req

class TestCRUD(unittest.TestCase):
    base_url = "http://127.0.0.1:5000/api/accounts"
    body = {
        "imie": "Jan",
        "nazwisko": "Kowalski",
        "pesel": "12345678901"
    }
    invalid_pesel = "11111111111"

    def setUp(self):
        req.delete(f"{self.base_url}/{self.body['pesel']}")
        req.post(self.base_url, json=self.body)

    def tearDown(self):
        req.delete(f"{self.base_url}/{self.body['pesel']}")
        req.delete(f"{self.base_url}/{self.invalid_pesel}")

    def test_create_acc(self):
        req.delete(f"{self.base_url}/{self.body['pesel']}")
        response = req.post(self.base_url, json=self.body)
        self.assertEqual(response.status_code, 201, "Wrong status code - account not created")
    
    def test_create_acc_promo(self):
        req.delete(f"{self.base_url}/{self.body['pesel']}")
        updated_body = {"imie": "Jan", "nazwisko": "Kowalski", "pesel": "12345678901", "promo": "PROM_XYZ"}
        response = req.post(self.base_url, json=updated_body)
        self.assertEqual(response.status_code, 201, "Wrong status code - account not created")
    
    def test_create_acc_taken(self):
        response = req.post(self.base_url, json=self.body)
        self.assertEqual(response.status_code, 409, "Wrong status code - account created")

    def test_findAcc(self):
        response = req.get(f"{self.base_url}/{self.body['pesel']}")
        self.assertEqual(response.status_code, 200, "Wrong status code - account should be found")

    def test_findAccFailure(self):
        response = req.get(f"{self.base_url}/{self.invalid_pesel}")
        self.assertEqual(response.status_code, 404, "Wrong status code - account should not be found")

    def test_updateAcc(self):
        updated_body = {"imie": "Ania", "nazwisko": "Roland"}
        response = req.patch(f"{self.base_url}/{self.body['pesel']}", json=updated_body)
        self.assertEqual(response.status_code, 200, "Wrong status code")
        
        updated = req.get(f"{self.base_url}/{self.body['pesel']}")
        self.assertEqual(updated.json()["imie"], "Ania", "Account update failed")
        self.assertEqual(updated.json()["nazwisko"], "Roland", "Account update failed")

    def test_updateAcc_Failure(self):
        updated_body = {"imie": "Ania", "nazwisko": "Roland"}
        response = req.patch(f"{self.base_url}/{self.invalid_pesel}", json=updated_body)
        self.assertEqual(response.status_code, 404, "Wrong status code")
        self.assertEqual(response.json()["message"], "Could not update the account", "Unexpected update message")

    def test_deleteAcc(self):
        response = req.delete(f"{self.base_url}/{self.body['pesel']}")
        self.assertEqual(response.status_code, 200, "Wrong status code")
        self.assertEqual(response.json()["message"], "Account deleted", "Account not deleted")

    def test_deleteAcc_Failure(self):
        response = req.delete(f"{self.base_url}/{self.invalid_pesel}")
        self.assertEqual(response.status_code, 404, "Wrong status code")
        self.assertEqual(response.json()["message"], "Could not delete the account", "Unexpected delete message")
