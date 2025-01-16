from src.trx.trx import Trx

from ecdsa import VerifyingKey

import hashlib
import base58


def serialize_trx(trx_data : Trx):
        
    input_string = trx_data._input_string()
    output_string = trx_data._output_string()


    str_data = str(Trx(input_string, output_string))

    return str_data

def get_address(pk : VerifyingKey):

    pk_string = pk.to_string()

    sha256_hash = hashlib.sha256(pk_string).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_hash)
    public_key_hash = ripemd160.digest()

    versioned_payload = b'\x00' + public_key_hash

    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]

    address_bytes = versioned_payload + checksum

    address = base58.b58encode(address_bytes).decode('utf-8')

    return address

def parse_transaction_data(transaction_data: str):
    # Split into input and output sections
    try:
        inputs_section, outputs_section = transaction_data.split("]:[")
    except ValueError:
        raise ValueError("Invalid transaction data format. Ensure it contains inputs and outputs.")

    # Helper function to process each section
    def process_section(section, section_type):
        # Clean the brackets and split items
        items = section.strip("[]").split("', '")
        parsed_items = []
        for item in items:
            try:
                # Extract the type, amount, and address
                prefix, value = item.split(", ", 1)
                amount, address = value.split(":")
                parsed_items.append({
                    "Type": section_type,
                    "Amount": int(amount),
                    "Address": address
                })
            except ValueError:
                raise ValueError(f"Unexpected format for item: {item}")
        return parsed_items

    # Process inputs and outputs
    inputs = process_section(inputs_section.strip("'"), "Input")
    outputs = process_section(outputs_section.strip("'"), "Output")

    # Combine the results
    return inputs + outputs
