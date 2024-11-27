class Konto:
    def __init__(self):
        self.saldo = 0
        self.historia = []
        self.oplata_ekspres = 0

    def przelew(self, adresat, kwota):
        if(self.saldo > kwota):
            self.saldo -= kwota
            adresat.saldo += kwota
            self.historia.append(kwota*-1)
            adresat.historia.append(kwota)
            return True
        return False

    def ekspres(self, adresat, kwota):
        if(self.saldo > kwota - self.oplata_ekspres):
            self.saldo = self.saldo - kwota - self.oplata_ekspres
            adresat.saldo += kwota
            self.historia.append(kwota*-1)
            self.historia.append(self.oplata_ekspres*-1)
            adresat.historia.append(kwota)
            return True
        return False
