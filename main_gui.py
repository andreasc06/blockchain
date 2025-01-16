import tkinter as tk
from tkinter import Toplevel, Listbox, Entry, Button
from src.block import Block
from src.network import Network
from src.wallet import Wallet
from src.node import Node
from src.wallets.adr_database import *
from src.miner import Miner
from src.trx.utxo import Utxo
from src.trx.trx import Trx
from src.util.crypto_util import parse_transaction_data

# Initialize blockchain components
network = Network()
node = Node(network)
miner = Miner(network, node)

genesis_input =  [Utxo(100, "COINBASE")]
genesis_output = [Utxo(100, ADDRESS_A)]

genesis_transactions = [Trx(genesis_input, genesis_output)]

print("\nMining genesis......")

genesis_block = Block(genesis_transactions, 
                      None, 
                      miner.mine_block(genesis_transactions, None), 
                      0)

network.broadcasted_blocks.append(genesis_block) 
node.listen_and_verify_block_broadcast()


def open_wallet_management_menu():
    def create_new_wallet():
        """Generate a new wallet with a random private key, public key, and address."""

        wallet = Wallet(network, node)
        submenu.destroy()
        open_wallet_menu(wallet)

    def import_wallet():
        """Import an existing wallet using a user-provided private key."""
        private_key = private_key_entry.get().strip()

        print(private_key)
        print(len(private_key))
        wallet = Wallet(network, node, private_key)

        submenu.destroy()

        open_wallet_menu(wallet)


    # Create the submenu
    submenu = Toplevel(root)
    submenu.title("Wallet Management")

    # Title Label
    title_label = tk.Label(submenu, text="Wallet Management", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Create New Wallet Button
    create_wallet_button = tk.Button(
        submenu,
        text="Create New Wallet",
        font=("Arial", 12),
        command=create_new_wallet,
    )
    create_wallet_button.pack(pady=10)

    # Import Wallet Section
    import_wallet_label = tk.Label(submenu, text="Import Wallet", font=("Arial", 14, "bold"))
    import_wallet_label.pack(pady=(20, 5))

    private_key_entry = tk.Entry(submenu, width=50, font=("Arial", 12))
    private_key_entry.pack(pady=5)

    import_wallet_button = tk.Button(
        submenu,
        text="Import Wallet",
        font=("Arial", 12),
        command=import_wallet,
    )
    import_wallet_button.pack(pady=10)

    # Wallet Info Display
    wallet_info_label = tk.Label(submenu, text="", font=("Arial", 12), justify="left", wraplength=600)
    wallet_info_label.pack(pady=(20, 10))

    # Close Button
    close_button = tk.Button(submenu, text="Close", command=submenu.destroy)
    close_button.pack(pady=20)

# Wallet Menu
def open_wallet_menu(wallet):

    def copy_to_clipboard(text):
        """Copy the given text to the clipboard."""
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()  # Keeps the clipboard data

    def send_transaction():
        selected_utxos = [wallet.utxos[int(idx)] for idx in utxo_list.curselection()]
        recipient_address = address_entry.get()
        amount_to_send = amount_entry.get()

        if not recipient_address:
            print("Please enter a recipient address.")
        elif not selected_utxos:
            print("Please select UTXOs to send.")
        elif not amount_to_send.isdigit() or int(amount_to_send) <= 0:
            print("Please enter a valid amount.")
        else:
            print(f"Sending {amount_to_send} coins to {recipient_address} using UTXOs: {selected_utxos}")
            wallet.send_transaction(recipient_address, int(amount_to_send), selected_utxos)
            node.listen_and_verify_trx_broadcast()
            network.clear_network()
            refresh_balance()

    def refresh_balance():
        # Save the indices of currently selected UTXOs
        selected_indices = utxo_list.curselection()

        wallet.get_utxos()
        balance_label.config(text=f"Balance: {wallet.get_balance()} coins")
        utxo_list.delete(0, tk.END)
        for idx, utxo in enumerate(wallet.utxos):
            utxo_text = f"UTXO {idx + 1}: Amount: {utxo.amount} coins"
            utxo_list.insert(tk.END, utxo_text)

        # Restore the previously selected UTXOs
        for idx in selected_indices:
            if idx < utxo_list.size():  # Ensure the index is still valid
                utxo_list.selection_set(idx)

        # Schedule the next update after 1 second
        submenu.after(1000, refresh_balance)

    submenu = Toplevel(root)
    submenu.title("Wallet")

    balance_label = tk.Label(submenu, text=f"Balance: {wallet.get_balance()} coins", font=("Arial", 14))
    balance_label.pack(padx=20, pady=10)

    utxo_label = tk.Label(submenu, text="Available UTXOs (Select to use):", font=("Arial", 12, "bold"))
    utxo_label.pack(pady=(10, 5))

    utxo_list = Listbox(submenu, selectmode=tk.MULTIPLE, height=8, width=50)
    utxo_list.pack(padx=20, pady=5)

    address_label = tk.Label(submenu, text="Recipient Address:", font=("Arial", 12, "bold"))
    address_label.pack(pady=(10, 5))

    address_entry = Entry(submenu, width=40)
    address_entry.pack(pady=5)

    amount_label = tk.Label(submenu, text="Amount to Send:", font=("Arial", 12, "bold"))
    amount_label.pack(pady=(10, 5))

    amount_entry = Entry(submenu, width=40)
    amount_entry.pack(pady=5)

    send_button = Button(submenu, text="Send", command=send_transaction)
    send_button.pack(pady=10)

    # Private Key
    private_key_frame = tk.Frame(submenu)
    private_key_label = tk.Label(private_key_frame, text=f"Private Key: {wallet.sk_hex}", font=("Arial", 10), justify="left")
    private_key_label.pack(side=tk.LEFT, padx=(0, 10))
    copy_private_key_button = tk.Button(private_key_frame, text="Copy", command=lambda: copy_to_clipboard(wallet.sk_hex))
    copy_private_key_button.pack(side=tk.LEFT)
    private_key_frame.pack(pady=(10, 2))

    # Public Key
    public_key_frame = tk.Frame(submenu)
    public_key_label = tk.Label(public_key_frame, text=f"Public Key: {wallet.pk_hex}", font=("Arial", 10), justify="left")
    public_key_label.pack(side=tk.LEFT, padx=(0, 10))
    copy_public_key_button = tk.Button(public_key_frame, text="Copy", command=lambda: copy_to_clipboard(wallet.pk_hex))
    copy_public_key_button.pack(side=tk.LEFT)
    public_key_frame.pack(pady=(10, 2))

    # Address
    address_frame = tk.Frame(submenu)
    address_label = tk.Label(address_frame, text=f"Address: {wallet.address}", font=("Arial", 10), justify="left")
    address_label.pack(side=tk.LEFT, padx=(0, 10))
    copy_address_button = tk.Button(address_frame, text="Copy", command=lambda: copy_to_clipboard(wallet.address))
    copy_address_button.pack(side=tk.LEFT)
    address_frame.pack(pady=(10, 2))

    close_button = tk.Button(submenu, text="Close", command=submenu.destroy)
    close_button.pack(pady=10)

    # Initialize the balance and UTXO list, and start periodic updates
    refresh_balance()


def open_mining_menu():
    def mine_block():
        # Get valid transaction indices based on the selection
        selected_indices = [line_to_trx[idx] for idx in mempool_list.curselection() if line_to_trx[idx] is not None]
        
        # Retrieve the corresponding transactions
        selected_transactions = [node.mempool[trx_idx] for trx_idx in set(selected_indices)]

        print("Mining block with the following transactions:")
        for trx in selected_transactions:
            parsed_data = parse_transaction_data(str(trx))  # Use parse function here
            for entry in parsed_data:
                print(f"{entry['Type']} - Amount: {entry['Amount']}, Address: {entry['Address']}")
        
        # Get the miner address from the entry field
        miner_address = miner_address_entry.get()
        
        if not miner_address:
            print("Please enter a miner address.")
            return
        
        # Create the new block
        if selected_transactions == None:
            selected_transactions = []

        selected_transactions.insert(0, Trx([Utxo(100, "COINBASE")], [Utxo(100, miner_address)]))

        print(selected_indices)
        new_block = Block(
            selected_transactions,
            node.blockchain[-1].calculate_block_hash(),
            miner.mine_block(selected_transactions, node.blockchain[-1].calculate_block_hash()), 
            node.blockchain[-1].index + 1
        )
        network.broadcasted_blocks.append(new_block)
        node.listen_and_verify_block_broadcast()
        network.clear_network()

    def refresh_mempool():
        """Refresh the mempool list periodically."""
        # Save current selection
        current_selection = mempool_list.curselection()

        # Clear and refresh the Listbox
        mempool_list.delete(0, tk.END)
        line_to_trx.clear()

        for trx_index, trx in enumerate(node.mempool):
            parsed_data = parse_transaction_data(str(trx))  # Parse the transaction
            for entry in parsed_data:
                display_str = f"{entry['Type']} - Amount: {entry['Amount']}, Address: {entry['Address']}"
                mempool_list.insert(tk.END, display_str)
                line_to_trx.append(trx_index)
            mempool_list.insert(tk.END, "")
            line_to_trx.append(None)

        # Restore selection after refresh
        for idx in current_selection:
            if idx < mempool_list.size():
                mempool_list.selection_set(idx)

        # Schedule the next refresh
        submenu.after(1000, refresh_mempool)

    def on_entry_select(event):
        """Highlight all lines tied to the same transaction."""
        selection = mempool_list.curselection()
        if not selection:
            return

        selected_index = selection[0]
        trx_index = line_to_trx[selected_index]

        mempool_list.selection_clear(0, tk.END)
        for line_index, line_trx_index in enumerate(line_to_trx):
            if line_trx_index == trx_index:
                mempool_list.selection_set(line_index)

    # Create the submenu
    submenu = Toplevel(root)
    submenu.title("Mempool")

    mempool_label = tk.Label(submenu, text="Mempool Transactions:\n", font=("Arial", 12, "bold"))
    mempool_label.pack(pady=(10, 5))

    mempool_list = Listbox(submenu, selectmode=tk.SINGLE, height=10, width=60)
    mempool_list.bind("<<ListboxSelect>>", on_entry_select)
    mempool_list.pack(padx=20, pady=5)

    line_to_trx = []

    # Add a label and entry field for the miner's address
    miner_address_label = tk.Label(submenu, text="Miner's Address:", font=("Arial", 12, "bold"))
    miner_address_label.pack(pady=(10, 5))

    miner_address_entry = Entry(submenu, width=40)
    miner_address_entry.pack(pady=5)

    mine_button = tk.Button(submenu, text="Mine Block", command=mine_block)
    mine_button.pack(pady=10)

    close_button = tk.Button(submenu, text="Close", command=submenu.destroy)
    close_button.pack(pady=10)

    # Start refreshing the mempool
    refresh_mempool()



def open_blockchain_viewer():
    def update_block_details(index):
        block = node.blockchain[index]
        prevhash_label.config(text=f"PrevHash: {block.prev_hash}")
        nonce_label.config(text=f"Nonce: {block.nonce}")
        block_index_label.config(text=f"Block {index + 1} of {len(node.blockchain)}")

        # Clear and update transaction list
        trx_listbox.delete(0, tk.END)
        for trx in block.trx:
            parsed_data = parse_transaction_data(str(trx))  # Use the parse function here
            trx_listbox.insert(tk.END, f"Transaction:")
            for entry in parsed_data:
                trx_listbox.insert(
                    tk.END, f"  {entry['Type']} - Amount: {entry['Amount']}, Address: {entry['Address']}"
                )
            trx_listbox.insert(tk.END, "")  # Empty line for spacing between transactions

    def on_slider_change(event):
        index = block_slider.get()
        update_block_details(index)

    viewer = Toplevel(root)
    viewer.title("Blockchain Viewer")

    block_index_label = tk.Label(viewer, text="", font=("Arial", 14, "bold"))
    block_index_label.pack(pady=10)

    prevhash_label = tk.Label(viewer, text="", font=("Arial", 12))
    prevhash_label.pack(pady=5)

    trx_label = tk.Label(viewer, text="Transactions:", font=("Arial", 12, "bold"))
    trx_label.pack(pady=(10, 5))

    trx_listbox = tk.Listbox(viewer, height=20, width=70)
    trx_listbox.pack(padx=20, pady=5)

    nonce_label = tk.Label(viewer, text="", font=("Arial", 12))
    nonce_label.pack(pady=5)

    block_slider = tk.Scale(
        viewer, from_=0, to=len(node.blockchain) - 1, orient=tk.HORIZONTAL, length=400,
        label="Navigate Blocks", showvalue=True, tickinterval=1
    )
    block_slider.pack(pady=20)
    block_slider.bind("<Motion>", on_slider_change)
    block_slider.bind("<ButtonRelease-1>", on_slider_change)

    close_button = tk.Button(viewer, text="Close", command=viewer.destroy)
    close_button.pack(pady=10)

    # Initialize with the first block
    if node.blockchain:
        update_block_details(0)
    else:
        block_index_label.config(text="No blocks in the blockchain.")
def open_keys_menu():
    def copy_to_clipboard(text):
        """Copy the given text to the clipboard."""
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()  # Keeps the clipboard data

    # Key data
    key_data = {
        "Key Pair A": {
            "Private Key": PRIVATE_KEY_A,
            "Public Key": PUBLIC_KEY_A,
            "Address": ADDRESS_A,
        },
        "Key Pair B": {
            "Private Key": PRIVATE_KEY_B,
            "Public Key": PUBLIC_KEY_B,
            "Address": ADDRESS_B,
        },
        "Key Pair C": {
            "Private Key": PRIVATE_KEY_C,
            "Public Key": PUBLIC_KEY_C,
            "Address": ADDRESS_C,
        },
    }

    submenu = Toplevel(root)
    submenu.title("Key Pairs")

    # Title Label
    title_label = tk.Label(submenu, text="Stored Key Pairs", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Add key data to the display
    for key_name, keys in key_data.items():
        # Key Name Header
        key_name_label = tk.Label(submenu, text=key_name, font=("Arial", 14, "bold"))
        key_name_label.pack(pady=(10, 0))

        # Display keys
        for key_type, key_value in keys.items():
            frame = tk.Frame(submenu)
            frame.pack(pady=(5, 0), padx=20, fill="x")

            # Key Label
            key_label = tk.Label(frame, text=f"{key_type}: {key_value}", anchor="w", justify="left", wraplength=600)
            key_label.pack(side="left", padx=10)

            # Copy Button
            copy_button = tk.Button(
                frame,
                text="Copy",
                command=lambda text=key_value: copy_to_clipboard(text),
            )
            copy_button.pack(side="right", padx=10)

    # Close Button
    close_button = tk.Button(submenu, text="Close", command=submenu.destroy)
    close_button.pack(pady=20)




# Main Menu
root = tk.Tk()
root.title("Blockchain")
root.geometry("600x550")

title_label = tk.Label(root, text="BLOCKCHAIN", font=("Arial", 40, "bold"))
title_label.pack(pady=10)

wallet_button = tk.Button(root, text="Wallet", font=("Arial", 30), command=open_wallet_management_menu)
wallet_button.pack(pady=(30, 10))

mempool_button = tk.Button(root, text="Mine Block", font=("Arial", 30), command=open_mining_menu)
mempool_button.pack(pady=10)

blockchain_button = tk.Button(root, text="Blockchain", font=("Arial", 30), command=open_blockchain_viewer)
blockchain_button.pack(pady=10)

keys_button = tk.Button(root, text="Keys and Addresses", font=("Arial", 30), command=open_keys_menu)
keys_button.pack(pady=10)

root.mainloop()
