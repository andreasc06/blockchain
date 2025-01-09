from src.network import Network
from ecdsa import VerifyingKey
import hashlib
import base58

class Node:

    def __init__(self, network : Network):

        self.network = network

        self.blockchain = []
        self.mempool = []
  
    def verify_transaction(self, pk : VerifyingKey, trx_data, signature):

        byte_data = str(trx_data).encode('utf-8')  # Encoding data to bytes
        tx_hash = hashlib.sha256(byte_data).digest()

        try:
            return pk.verify(signature, tx_hash)
        except:
            return False
        
    def verify_address(self, pk : VerifyingKey, target_address):

        pk_string = pk.to_string()

        sha256_hash = hashlib.sha256(pk_string).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        public_key_hash = ripemd160.digest()
        versioned_payload = b'\x00' + public_key_hash
        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
        address_bytes = versioned_payload + checksum

        address = base58.b58encode(address_bytes).decode('utf-8')

        return True if address == target_address else False

    def listen_and_verify_broadcast(self):

        for trx in self.network.broadcasted_trx:

            pk =  trx[0]
            trx_data = trx[1]
            signature = trx[2]

            from_adr = str(trx_data).split(':')[0]

            if self.verify_transaction(pk, trx_data, signature) and self.verify_address(pk, from_adr):

                self.mempool.append(trx)

        