class Accounts_Registry():
    def __init__(self):
        self.registry = []
    
    def AddAccount(self, account):
        self.registry.append(account)
    
    def SearchAccount(self, test_pesel):
        for person in self.registry:
            if person.pesel == test_pesel:
                return person
        return "Nie znaleziono konta z podanym peselem"

    def CountAccount(self):
        return len(self.registry)