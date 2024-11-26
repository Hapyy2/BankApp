from app.Konto_osobiste import Konto_osobiste

class Accounts_Registry():
    registry = []
    
    @classmethod
    def AddAccount(cls, account):
        cls.registry.append(account)
    
    @classmethod
    def SearchAccount(cls, test_pesel):
        for person in cls.registry:
            if person.pesel == test_pesel:
                return person
        return "Nie znaleziono konta z podanym peselem"

    @classmethod
    def CountAccount(cls):
        return len(cls.registry)
    
    @classmethod
    def UpdateAccount(cls, pesel, data):
        person = cls.SearchAccount(pesel)
        if isinstance(person, Konto_osobiste):
            if "imie" in data:
                person.imie = data["imie"]
            if "nazwisko" in data:
                person.nazwisko = data["nazwisko"]
            if "pesel" in data:
                person.pesel = data["pesel"]
            return True
        return False
    
    @classmethod
    def DeleteAccount(cls, pesel):
        person = cls.SearchAccount(pesel)
        if isinstance(person, Konto_osobiste):
            cls.registry.remove(person)
            return True
        return False