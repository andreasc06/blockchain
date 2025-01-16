from src.network import Network
from src.node import Node
from src.trx.trx import Trx
from src.trx.utxo import Utxo
from src.wallets.adr_database import ADDRESS_A

from src.util.crypto_util import get_address, serialize_trx

from ecdsa import SigningKey, SECP256k1
import hashlib
import itertools


class Wallet():

    def __init__(self, network : Network, node : Node, sk : str = None):

        self.sk_raw = None
        self.pk_raw = None
        self.address = None

        self.sk_hex = None
        self.pk_hex = None

        self.network = network

        self.utxos = []

        self.node = node

        self.import_key(sk) if sk != None else self.create_key()
        self.get_utxos()

    def get_balance(self):

        balance = 0

        for utxo in self.utxos:
            
            balance += utxo.amount

        return balance
    
    def get_utxos(self):

        self.utxos = []

        for utxo in self.node.utxo_pool:

            if utxo.assigned_adr == self.address:

                self.utxos.append(utxo)

    def import_key(self, sk):

        self.sk_raw = SigningKey.from_string(bytes.fromhex(sk), curve=SECP256k1)
        self.create_wallet(self.sk_raw)

    def create_key(self):

        self.sk_raw = SigningKey.generate(curve=SECP256k1)

        self.create_wallet(self.sk_raw)

    def create_wallet(self, sk : SigningKey):

        self.pk_raw = sk.get_verifying_key()
        self.address = get_address(self.pk_raw)

        self.sk_hex = self.sk_raw.to_string().hex()
        self.pk_hex = self.pk_raw.to_string().hex()


    def sign_transaction(self, sk : SigningKey, trx_data):

        byte_data = trx_data.encode('utf-8')  # Encoding data to bytes

        tx_hash = hashlib.sha256(byte_data).digest()

        signature = sk.sign(tx_hash)

        return signature
    

    def send_transaction(self, rec_adr, amount, utxos):

        input_amount = sum(utxo.amount for utxo in utxos)

        input_utxo = utxos
        output_utxo = [Utxo(amount, rec_adr), Utxo(input_amount - amount, self.address)]
        trx_data = Trx(input_utxo, output_utxo)

        sig_data = serialize_trx(trx_data)

        signature = self.sign_transaction(self.sk_raw, sig_data)

        self.network.trx_broadcast([self.pk_raw, trx_data, signature])


