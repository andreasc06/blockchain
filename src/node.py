from src.network import Network

from src.util.crypto_util import get_address, serialize_trx
from src.block import Block
from src.trx.utxo import Utxo
from ecdsa import VerifyingKey

import hashlib


class Node:

    def __init__(self, network : Network):

        self.network = network

        self.blockchain = []
        self.mempool = []

        self.utxo_pool = []


    def get_all_utxos(self):

        for block in self.blockchain:

            for trx in block.trx:

                for output in trx.output:

                    self.utxo_pool.append(output)

  
    def verify_transaction(self, pk : VerifyingKey, trx_data, signature):

        byte_data = (trx_data).encode('utf-8')  # Encoding data to bytes
        tx_hash = hashlib.sha256(byte_data).digest()

        try:
            return pk.verify(signature, tx_hash)
        except:
            return False
        
        
    def verify_address(self, inputs, target_adr):

        for input in inputs:

            if input.assigned_adr != target_adr:

                return False
            
        return True
    

    def listen_and_verify_trx_broadcast(self):

        for trx in self.network.broadcasted_trx:

            pk =  trx[0]
            trx_data = trx[1]
            signature = trx[2]

            from_adr = get_address(pk)
   
            sig_data = serialize_trx(trx_data)


            if self.verify_transaction(pk, sig_data, signature) and self.verify_address(trx_data.input, from_adr):

                self.mempool.append(trx_data)
                print("BROADCASTED TRX VERIFIED")

    def listen_and_verify_block_broadcast(self):

        for block in self.network.broadcasted_blocks:

            if self.verify_hash(block) and self.verify_trx(block) and block not in self.blockchain:

                print("BROADCASTED BLOCK VERIFIED")
                self.blockchain.append(block)

    def verify_hash(self, block : Block):

        if block.calculate_block_hash().startswith("0" * self.network.dif):

            print("BLOCK HASH VERIFIED")
            return True
        
    def verify_trx(self, block : Block):

        for trx in block.trx:

            trx_index = 1
            input_utxos = []
            input_sum = 0
            output_sum = 0

            for input in trx.input:

                input_utxos.append(input)
                input_sum += input.amount

            for output in trx.output:

                output_sum += output.amount

            UTXO_IN_POOL = all(input in self.utxo_pool for input in input_utxos[1:])
            IS_COINBASE_BLOCK = (input_utxos[0].assigned_adr == "COINBASE" and input_utxos[0].amount == self.network.block_reward and trx_index == 1)

            if not ((input_sum == output_sum) and (UTXO_IN_POOL or IS_COINBASE_BLOCK)):

                return False

            trx_index += 1

        print("TRX IN BLOCK VERIFIED")
        return True

            

            
            






            

        







