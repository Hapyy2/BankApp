from app.Konto import *
import requests as req
from datetime import datetime
import os

class Konto_firmowe(Konto):
    def __init__(self, nazwa, NIP):
        super().__init__()
        self.nazwa = nazwa
        self.NIP = NIP
        self.oplata_ekspres = 5
        self.test_NIP()
        if self.NIP != "Niepoprawny NIP!":
            if self.checkNIP() == False:
                raise ValueError("Company not registered!!")

    def test_NIP(self):
        if len(self.NIP) != 10:
            self.NIP = "Niepoprawny NIP!"
    
    def zaciagnij_kredyt(self, kwota):
        if self.war_kredyt_1(kwota) and self.war_kredyt_2():
            self.saldo += kwota
            self.historia.append(kwota)
    
    def war_kredyt_1(self, kwota):
        return self.saldo >= kwota*2

    def war_kredyt_2(self):
        return 1775 in self.historia
    
    def checkNIP(self):
        MF_URL = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/api/search/nip/")
        data = datetime.today().strftime('%Y-%m-%d')
        response = req.get(f'{MF_URL}{self.NIP}?date={data}')
        if response.status_code == 200:
            return True
        return False

