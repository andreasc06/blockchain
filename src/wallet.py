from ecdsa import SigningKey, VerifyingKey, SECP256k1
import base58
import hashlib

class Wallet():

    def __init__(self, pk : str = None):

        self.sk_raw = None
        self.pk_raw = None
        self.address = None

        self.sk_hex = None
        self.pk_hex = None

        self.import_key(pk) if pk != None else self.create_key()

    def import_key(self, sk):

        self.sk_raw = SigningKey.from_string(bytes.fromhex(sk), curve=SECP256k1)
        self.create_wallet(self.sk_raw)


    def create_key(self):

        self.sk_raw = SigningKey.generate(curve=SECP256k1)

        self.create_wallet(self.sk_raw)

    def create_wallet(self, sk : SigningKey):

        self.pk_raw = sk.get_verifying_key()
        self.address = self.get_address(self.pk_raw.to_string())

        self.sk_hex = self.sk_raw.to_string().hex()
        self.pk_hex = self.pk_raw.to_string().hex()

    def get_address(self, pk : str):

        sha256_hash = hashlib.sha256(pk).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        public_key_hash = ripemd160.digest()

        versioned_payload = b'\x00' + public_key_hash

        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]

        address_bytes = versioned_payload + checksum

        address = base58.b58encode(address_bytes).decode('utf-8')
        return address

    def sign_transaction(self, sk : SigningKey, trx_data):

        byte_data = trx_data.encode('utf-8')  # Encoding data to bytes

        tx_hash = hashlib.sha256(byte_data).digest()

        signature = sk.sign(tx_hash)

        return signature

    def verify_transaction(self, pk : VerifyingKey, trx_data, signature):

        # Will be moves in the futures cause validations dosent happen in wallet.

        byte_data = trx_data.encode('utf-8')  # Encoding data to bytes
        tx_hash = hashlib.sha256(byte_data).digest()

        try:
            return pk.verify(signature, tx_hash)
        except:
            return False



wallet = Wallet()


print("Your private key:", wallet.sk_hex)
print("Your public key:", wallet.pk_hex)
print("Your address:", wallet.address)

