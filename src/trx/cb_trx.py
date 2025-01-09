# Transaction Object for making new coins. Meant to be used for block reward, but also used for the genesis block for starting funds

class CoinBaseTrx:

    def __init__(self, amount, rec_adr):

        self.amount = amount
        self.rec_adr = rec_adr