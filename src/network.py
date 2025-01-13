from src.block import Block
# Simulated internett. Just a Object where broadcastet transactions are stored and where nodes can add transaction to mempool

class Network:

    def __init__(self):

        self.broadcasted_trx = []
        self.broadcasted_blocks = []

        self.dif = 4
        self.block_reward = 100

    def trx_broadcast(self, trx_data : list):

        self.broadcasted_trx.append(trx_data)

    def block_broadcast(self, block : Block):

        self.broadcasted_blocks.append(block)

