from src.block import Block
from src.network import Network
from src.wallet import Wallet
from src.node import Node
from src.wallets.adr_database import *

from src.miner import Miner

import time

from src.trx.utxo import Utxo
from src.trx.trx import Trx

network = Network()
node = Node(network)
miner = Miner(network, node)
wallet = Wallet(network, node, "0a9f0176251c8be806dd7980bc80c59d14a30fbf426b3dc577092ea10477a4ee") # KEY for Wallet A


genesis_input =  [Utxo(100, "COINBASE")]
genesis_output = [Utxo(50, ADDRESS_A),
                  Utxo(30, ADDRESS_B), 
                  Utxo(20, ADDRESS_C)]

genesis_transactions = [Trx(genesis_input, genesis_output)]

genesis_block = Block(genesis_transactions, 
                      None, 
                      miner.mine_block(genesis_transactions, None), 
                      0)



network.broadcasted_blocks.append(genesis_block) 
node.listen_and_verify_block_broadcast()

time.sleep(2)

node.get_all_utxos()
wallet.get_utxos()

wallet.send_transaction("1KgBbcrskBsxvaKkN94jL3oNxRj4LDAk3J", 50)
node.listen_and_verify_trx_broadcast()

next_block = Block(node.mempool,      
                   genesis_block.calculate_block_hash(), 
                   miner.mine_block(node.mempool, genesis_block.calculate_block_hash()), 
                   1)


network.broadcasted_blocks.append(next_block) 
node.listen_and_verify_block_broadcast()

print(node.blockchain)


