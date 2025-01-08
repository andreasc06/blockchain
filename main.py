from src.block import Block

from src.miner import mine_block

dif = 4

mempool = [
    ["Alice pays 7$ to Bob", "Bob pays 2$ to Walter,", "Jesse pays 8$ to Walter"],  # Block 1
    ["Bob pays 8$ to Alice", "Trump pays 2$ to Obama,", "Walter pays 100$ to Gus"],  # Block 2
    ["Alice pays 5$ to Charlie", "Walter pays 3$ to Sarah", "Bob pays 10$ to Alice"],  # Block 3
    ["Jesse pays 20$ to Walter", "Trump pays 3$ to Bob", "Charlie pays 15$ to Obama"],  # Block 4
    ["Walter pays 7$ to Gus", "Alice pays 9$ to Jesse", "Bob pays 2$ to Sarah"],  # Block 5
    ["Charlie pays 12$ to Alice", "Obama pays 5$ to Walter", "Bob pays 1$ to Trump"],  # Block 6
    ["Jesse pays 25$ to Bob", "Walter pays 4$ to Sarah", "Charlie pays 8$ to Obama"],  # Block 7
    ["Trump pays 13$ to Walter", "Bob pays 14$ to Alice", "Jesse pays 9$ to Gus"],  # Block 8
    ["Sarah pays 7$ to Charlie", "Bob pays 6$ to Obama", "Walter pays 10$ to Jesse"],  # Block 9
    ["Gus pays 5$ to Trump", "Charlie pays 8$ to Bob", "Alice pays 3$ to Walter"]  # Block 10
]



genesis_block = Block("GENESIS", None, mine_block("GENESIS", None, dif), 0)

blockchain = [genesis_block]

for trx in mempool:
    prev_block = blockchain[-1]
    noonce = mine_block(trx, prev_block.calculate_block_hash(), dif)

    new_block = Block(trx, prev_block.calculate_block_hash(), noonce, prev_block.index + 1)
    blockchain.append(new_block)

print("\n")

for block in blockchain:

    print("Block " + str(block.index))
    print("TRX: " + str(block.trx))
    print("PREV_HASH: " + str(block.prev_hash))
    print("NONCE: "+ str(block.nonce))
    print("HASHED_BLOCK: " + str(block.calculate_block_hash()))
    print("BLOCK DATA: " + f"{block.prev_hash}{block.trx}{block.nonce}")
    print("\n") 

