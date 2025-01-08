import hashlib

class Block:

    def __init__(self, trx, prev_hash, nonce, i):

        self.trx = trx
        self.prev_hash = prev_hash
        self.nonce = nonce
        
        self.index = i

    def calculate_block_hash(self):

        block_data = f"{self.prev_hash}{self.trx}{self.nonce}"
        return hashlib.sha256(block_data.encode()).hexdigest()

    