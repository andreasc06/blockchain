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
                  Utxo(30, ADDRESS_A), 
                  Utxo(20, ADDRESS_C)]

genesis_transactions = [Trx(genesis_input, genesis_output)]

print("\nMining genesis......")

genesis_block = Block(genesis_transactions, 
                      None, 
                      miner.mine_block(genesis_transactions, None), 
                      0)

network.broadcasted_blocks.append(genesis_block) 
node.listen_and_verify_block_broadcast()

wallet.get_utxos()

print("\n UTXO in circulation")
for utxo in node.utxo_pool:

    print(utxo.amount, utxo.assigned_adr)

print("\nSending 60 to", ADDRESS_B, "form", ADDRESS_A)

wallet.send_transaction(ADDRESS_B, 80, [Utxo(50, wallet.address), Utxo(30, wallet.address)])
node.listen_and_verify_trx_broadcast()
network.clear_network()

print("\nMining block......")

next_block = Block(node.mempool,      
                   genesis_block.calculate_block_hash(), 
                   miner.mine_block(node.mempool, genesis_block.calculate_block_hash()), 
                   1)

print("\nBroadcasting block..\n")

network.broadcasted_blocks.append(next_block)   
node.listen_and_verify_block_broadcast()
network.clear_network()
wallet.get_utxos()

print("\n UTXO in circulation")
for utxo in node.utxo_pool:

    print(utxo.amount, utxo.assigned_adr)

