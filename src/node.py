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

    def update_utxos(self):

        for trx in self.blockchain[-1].trx:

            for input in trx.input:

                if input.assigned_adr != "COINBASE":

                    self.utxo_pool.remove(input)

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


            if self.verify_transaction(pk, sig_data, signature) and self.verify_address(trx_data.input, from_adr) and self.valid_trx(trx_data):

                self.mempool.append(trx_data)
                print("BROADCASTED TRX VERIFIED")
            else:
                print("TRX: ", str(trx_data), "rejeted...")

    def listen_and_verify_block_broadcast(self):

        for block in self.network.broadcasted_blocks:

            if self.valid_hash(block) and self.valid_trx_in_block(block) and block not in self.blockchain:

                print("BROADCASTED BLOCK VERIFIED AND ADDED TO CHAIN")
                self.blockchain.append(block)
                self.update_utxos()
                self.remove_block_trx_from_mempool(block)
                for trx in self.mempool:
                    if not self.valid_trx(trx):
                        self.mempool.remove(trx)


    def remove_block_trx_from_mempool(self, block):

        for trx in block.trx:
            IS_COINBASE_TRX = (trx.input[0].assigned_adr == "COINBASE")
            if not IS_COINBASE_TRX:

                self.mempool.remove(trx)

    def valid_hash(self, block : Block):

        if block.calculate_block_hash().startswith("0" * self.network.dif):

            print("valid hash.....")
            return True
        else:
            print("invalid block hash.....")
            return False   
        
    def valid_trx(self, trx):


        input_sum = 0
        output_sum = 0
        input_utxos = []
        output_utxos = []
        for input in trx.input:

            input_utxos.append(input)
            input_sum += input.amount
                                    
        for output in trx.output:

            output_utxos.append(output)
            output_sum += output.amount

        

        IS_NEGATIVE_VALUES = (any(x.amount < 0 for x in output_utxos) or any(x.amount < 0 for x in input_utxos)) # Prevents spending/making negative UTXOs

        UTXO_IN_POOL = all(input in self.utxo_pool for input in input_utxos)

        return True if (input_sum == output_sum) and UTXO_IN_POOL and not IS_NEGATIVE_VALUES else False
            
        
    def valid_trx_in_block(self, block : Block):

        trx_index = 0

        for trx in block.trx:

            IS_COINBASE_TRX = (trx.input[0].assigned_adr == "COINBASE") and trx_index == 0

            if not self.valid_trx(trx) and not IS_COINBASE_TRX:
                print("invalid trx in block.....")
                return False
            
        print("valid trx in block.....")
        return True

            

            
            






            

        







