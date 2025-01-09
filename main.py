from src.block import Block
from src.network import Network
from src.wallet import Wallet
from src.node import Node
from adr import *

from src.miner import mine_block

from src.trx.cb_trx import CoinBaseTrx

network = Network()
node = Node(network)
wallet = Wallet(network)

dif = 1

genesis_transactions = [CoinBaseTrx(100, ADDRESS_A), CoinBaseTrx(50, ADDRESS_B), CoinBaseTrx(10, ADDRESS_C)]
genesis_block = Block(genesis_transactions, None, mine_block(genesis_transactions, None, dif), 0)

node.blockchain.append(genesis_block)
wallet.send_transaction(ADDRESS_A, 50)
node.listen_and_verify_broadcast()

