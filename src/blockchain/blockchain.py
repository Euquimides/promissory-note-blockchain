"""
Blockchain example code based on the tutorial at https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
Author: Daniel van Flymen
Modified by: Juan Carlos Vásquez D.
"""

import hashlib as hasher
import datetime as date
import json


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash="0")

    def new_block(self, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(date.datetime.now()),
            "transactions": self.current_transactions,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, doc_hash, description):
        self.current_transactions.append(
            {
                "sender": sender,
                "recipient": recipient,
                "doc_hash": doc_hash,
                "description": description,
            }
        )
        return self.last_block["index"] + 1

    # Get transaction details
    def get_transaction(self, index):
        return self.chain[index - 1]["transactions"]

    # Clear the blockchain
    def clear(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash="0")

    # Verify the blockchain
    def verify(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block["previous_hash"] != self.hash(
                previous_block
            ):  # Check if the previous hash is correct by hashing the previous block
                return False
        return True

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hasher.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
