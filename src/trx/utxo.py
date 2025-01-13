"""
UTXO object that holds the amount and owners address

"""

class Utxo:


    def __init__(self, amount, assigned_adr):
        self.amount = amount
        self.assigned_adr = assigned_adr

    def __str__(self):
        return f"{self.amount}:{self.assigned_adr}"

    def __eq__(self, other):

        """ To compare UTXO classes as values stored inside (not memory location)"""

        if not isinstance(other, Utxo):
            return False
        return (
            self.amount == other.amount and
            self.assigned_adr == other.assigned_adr
        )
