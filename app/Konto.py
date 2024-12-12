from datetime import datetime
from app.SMTPClient import SMTPClient

class Konto:
    def __init__(self):
        self.saldo = 0
        self.historia = []
        self.oplata_ekspres = 0
        self.history_message = ""

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

    def send_history_to_email(self, adresat, client: SMTPClient):
        data = datetime.today().strftime('%Y-%m-%d')
        subject = f"Wyciąg z dnia {data}"
        text = f"{self.history_message}: {self.historia}"
        response = client.send(subject, text, adresat)
        return response
