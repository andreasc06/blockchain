"""
UTXO object that holds the amount and owners address

"""


class Utxo:

    def __init__(self, amount, assigned_adr):

        self.amount = amount
        self.assigned_adr = assigned_adr

    def __str__(self):
        
        return f"{self.amount}:{self.assigned_adr}"