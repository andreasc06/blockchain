import hashlib
import random

def mine_block(trx, prev_hash, dif):

    target = "0" * dif
    nonce = 0

    tries = 0
    
    while True:

        nonce = random.randint(0, 4294967295)
        block_data = f"{prev_hash}{trx}{nonce}"

        hashed_nonce = hashlib.sha256(block_data.encode()).hexdigest()
        print(hashed_nonce)

        tries += 1

        if hashed_nonce.startswith(target):

            print(tries)

            return nonce
        
            