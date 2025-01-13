import hashlib
import random

from src.network import Network
from src.node import Node


class Miner:

    def __init__(self, network : Network, node : Node):

        self.node = node
        self.network = network


    def mine_block(self, trx, prev_hash):

        target = "0" * self.network.dif
        nonce = 0
        
        while True:

            nonce = random.randint(0, 4294967295)
            block_data = f"{prev_hash}{trx}{nonce}"

            hashed_nonce = hashlib.sha256(block_data.encode()).hexdigest()
            print(hashed_nonce)

            if hashed_nonce.startswith(target):

                return nonce
