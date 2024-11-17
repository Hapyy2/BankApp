from app.Konto import *

class Konto_firmowe(Konto):
    def __init__(self, nazwa, NIP):
        super().__init__()
        self.nazwa = nazwa
        self.NIP = NIP
        self.oplata_ekspres = 5
        self.test_NIP()

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