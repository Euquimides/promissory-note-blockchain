import requests
from enum import Enum

"""
This script demonstrates the process of creating a promissory note, signing and encrypting it, transferring it to another party, and accepting it.
"""


class BaseURL(Enum):
    BLOCKCHAIN_API_URL = "http://localhost:8001"
    XML_PROCESSOR_API_URL = "http://localhost:8002"


class PromissoryNote:
    def __init__(self, doc_path, description):
        self.doc_path = doc_path
        self.description = description

    def sign_and_encrypt_note(self, owner, key) -> str:
        # Add ownership to the promissory note
        ownership = requests.post(
            f"{BaseURL.XML_PROCESSOR_API_URL.value}/xml/add-ownership",
            files={"xml_file": open(self.doc_path, "rb")},
            data={"owner": owner, "owned_by_file_path": self.doc_path + ".owned"},
        )
        # Get owned_by_file_path
        owned_by_file_path = ownership.json()[
            "owned_by_file_path"
        ]  # src/data/promissory_note.xml.owned

        # Sign the promissory note with the new ownership
        signed_note = requests.post(
            f"{BaseURL.XML_PROCESSOR_API_URL.value}/xml/sign",
            files={"xml_file": open(owned_by_file_path, "rb")},
            data={"signed_xml_file_path": owned_by_file_path + ".signed"},
        )
        # Get signed_note path
        signed_note_path = signed_note.json()[
            "signed_xml_file_path"
        ]  # src/data/promissory_note.xml.owned.signed

        # Encrypt the promissory note
        encrypted_note = requests.post(
            f"{BaseURL.XML_PROCESSOR_API_URL.value}/xml/encrypt",
            files={"xml_file": open(signed_note_path, "rb")},
            data={"encrypted_xml_file_path": signed_note_path + ".enc", "key": key},
        )

        # Return encrypted_note path
        return encrypted_note.json()[
            "encrypted_xml_file_path"
        ]  # src/data/promissory_note.xml.owned.signed.enc

    def generate_hash(self, encrypted_note_path):
        # Generate a hash for the promissory note
        hash_value = requests.post(
            f"{BaseURL.XML_PROCESSOR_API_URL.value}/xml/generate-hash",
            files={"xml_file": open(encrypted_note_path, "rb")},
        )
        return hash_value.json()["hash"]

    def transfer_promissory_note(self, sender, recipient, hash_value):
        # Create a new transaction for the promissory note
        requests.post(
            f"{BaseURL.BLOCKCHAIN_API_URL.value}/transactions/new",
            json={
                "sender": sender,
                "recipient": recipient,
                "doc_hash": hash_value,
                "description": self.description,
            },
        )

        # Create a new block for the transaction
        block = requests.post(f"{BaseURL.BLOCKCHAIN_API_URL.value}/blocks/new")

        # Verify the transaction
        transaction = requests.get(f"{BaseURL.BLOCKCHAIN_API_URL.value}/chain")

        if transaction.json()["chain"][-1]["transactions"][0]["doc_hash"] != hash_value:
            raise ValueError("Transaction failed")

        return block.json()

    def accept_promissory_note(self, recipient, encrypted_note_path, key):
        # Decrypt the promissory note
        decrypted_note = requests.post(
            f"{BaseURL.XML_PROCESSOR_API_URL.value}/xml/decrypt",
            files={"encrypted_xml_file_path": open(encrypted_note_path, "rb")},
            data={"decrypted_xml_file_path": encrypted_note_path + ".dec", "key": key},
        )
        decrypted_note_path = decrypted_note.json()[
            "decrypted_xml_file_path"
        ]  # src/data/promissory_note.xml.owned.signed.enc.dec

        # Change the ownership of the promissory note
        new_owner_note = requests.post(
            f"{BaseURL.XML_PROCESSOR_API_URL.value}/xml/change-ownership",
            files={"xml_file": open(decrypted_note_path, "rb")},
            data={
                "new_owner": recipient,
                "owned_by_file_path": decrypted_note_path + ".owned",
            },
        )
        new_owner_note_path = new_owner_note.json()[
            "owned_by_file_path"
        ]  # src/data/promissory_note.xml.owned.signed.enc.dec.owned

        # Verify the new owner of the promissory note
        owner = requests.post(
            f"{BaseURL.XML_PROCESSOR_API_URL.value}/xml/verify-owner",
            params={"xml_file_path": new_owner_note_path},
        )

        return owner.json()["owner"]


def transaction_example(sender, recipient, doc_path, description, key):
    # Create a new promissory note
    promissory_note = PromissoryNote(doc_path, description)

    # Sign and encrypt the promissory note
    encrypted_note_path = promissory_note.sign_and_encrypt_note(sender, key)
    print("Encrypted note path:", encrypted_note_path)

    # Generate a hash for the promissory note
    hash_value = promissory_note.generate_hash(encrypted_note_path)
    print("\nPromissory note hash:", hash_value)

    # Transfer the promissory note
    block = promissory_note.transfer_promissory_note(sender, recipient, hash_value)
    print("\nPromissory note transferred to:", recipient)
    print("\nNew block forged:", block)

    # Accept the promissory note
    new_owner = promissory_note.accept_promissory_note(
        recipient, encrypted_note_path, key
    )
    print("\nPromissory note verified and accepted by:", new_owner)

    # Get the chain
    chain = requests.get(f"{BaseURL.BLOCKCHAIN_API_URL.value}/chain")
    print("\nBlockchain chain:", chain.json())


def main():
    key = requests.post(f"{BaseURL.XML_PROCESSOR_API_URL.value}/xml/generate-key")
    transaction_example(
        "Alice",
        "Bob",
        "src/data/promissory_note.xml",
        "Promissory note",
        key.json()["key"],
    )
    transaction_example(
        "Bob",
        "Charlie",
        "src/data/promissory_note.xml",
        "Promissory note",
        key.json()["key"],
    )
    transaction_example(
        "Charlie",
        "Alice",
        "src/data/promissory_note.xml",
        "Promissory note",
        key.json()["key"],
    )


if __name__ == "__main__":
    main()
