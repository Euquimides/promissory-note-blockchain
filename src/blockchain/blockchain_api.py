from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from blockchain import Blockchain

app = FastAPI()

# Initialize a new blockchain
blockchain = Blockchain()


class Transaction(BaseModel):
    sender: str
    recipient: str
    doc_hash: str
    description: Optional[str] = None


@app.post("/transactions/new")
def new_transaction(transaction: Transaction):
    index = blockchain.new_transaction(
        sender=transaction.sender,
        recipient=transaction.recipient,
        doc_hash=transaction.doc_hash,
        description=transaction.description,
    )
    return {"message": f"Transaction will be added to Block {index}"}


@app.get("/chain")
def full_chain():
    return {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }


@app.post("/blocks/new")
def new_block():
    last_block = blockchain.last_block
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(previous_hash=previous_hash)
    return {"message": "New block forged", "block": block}


@app.post("/clear")
def clear():
    blockchain.clear()
    return {"message": "Blockchain cleared"}


@app.get("/verify")
def verify():
    verified = blockchain.verify()
    return {"message": "Blockchain verified", "verified": verified}


@app.get("/")
def read_root():
    return {"message": "Welcome to the Blockchain API"}
