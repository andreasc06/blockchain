from src.network import Network

from src.util.crypto_util import get_address, serialize_trx

from ecdsa import VerifyingKey

import hashlib


class Node:

    def __init__(self, network : Network):

        self.network = network

        self.blockchain = []
        self.mempool = []

        self.utxo_pool = []


    def assign_utxos(self):

        for block in self.blockchain:

            for trx in block.trx:

                self.utxo_pool.append(trx)

  
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
    

    def listen_and_verify_broadcast(self):

        for trx in self.network.broadcasted_trx:

            pk =  trx[0]
            trx_data = trx[1]
            signature = trx[2]

            from_adr = get_address(pk)
   
            sig_data = serialize_trx(trx_data)


            if self.verify_transaction(pk, sig_data, signature) and self.verify_address(trx_data.input, from_adr):

                self.mempool.append(trx_data)
                print("verified")

