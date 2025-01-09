# Transaction Object for where there is a sender and reciver

class Trx:

    def __init__(self, from_adr, amount, rec_adr):

        self.from_adr = from_adr
        self.amount = amount
        self.rec_adr = rec_adr

    def __str__(self):
        
        return f"{self.from_adr}:{self.amount}:{self.rec_adr}"