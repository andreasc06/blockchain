from ecdsa import SigningKey, VerifyingKey, SECP256k1
import base58
import hashlib

def get_address(pk):

    sha256_hash = hashlib.sha256(pk).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_hash)
    public_key_hash = ripemd160.digest()

    versioned_payload = b'\x00' + public_key_hash

    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]

    address_bytes = versioned_payload + checksum

    address = base58.b58encode(address_bytes).decode('utf-8')
    return address

def sign_transaction(sk : SigningKey, trx_data):

    byte_data = trx_data.encode('utf-8')  # Encoding data to bytes

    tx_hash = hashlib.sha256(byte_data).digest()

    signature = sk.sign(tx_hash)

    return signature

def verify_transaction(pk : VerifyingKey, trx_data, signature):

    # Will be moves in the futures cause validations dosent happen in wallet.

    byte_data = trx_data.encode('utf-8')  # Encoding data to bytes
    tx_hash = hashlib.sha256(byte_data).digest()

    try:
        return pk.verify(signature, tx_hash)
    except:
        return False



raw_sk = SigningKey.generate(curve=SECP256k1)
raw_pk = raw_sk.get_verifying_key()


sk = raw_sk.to_string().hex()
pk = raw_pk.to_string().hex()

address = get_address(raw_pk.to_string())

print("Your private key:", sk)
print("Your public key:", pk)
print("Your address:", address)

