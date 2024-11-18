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