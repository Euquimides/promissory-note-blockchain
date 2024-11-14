import signxml
import hashlib
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from lxml import etree

"""
This class provides methods to sign and verify XML files, add, change, and remove ownership of XML files, generate and verify hash values of XML files, and symmetrically encrypt and decrypt XML files.
"""


class XMLProcessor:
    def __init__(self):
        load_dotenv(dotenv_path="src/.env")
        self.private_key_path = os.getenv("PRIVATE_KEY_PATH")
        self.cert_path = os.getenv("CERT_PATH")

    def sign_xml(self, xml_file_path, signed_xml_file_path):
        with open(xml_file_path, "rb") as xml_file:
            xml_data = xml_file.read()

        # Parse the XML data into an element
        xml_element = etree.fromstring(xml_data)

        private_key = open(self.private_key_path, "rb").read()
        # Sign the XML element instead of the raw data
        signed_xml_element = signxml.XMLSigner().sign(xml_element, key=private_key)

        # Convert the signed XML element to a byte string
        signed_xml_data = etree.tostring(
            signed_xml_element, encoding="UTF-8", xml_declaration=True
        )

        with open(signed_xml_file_path, "wb") as signed_xml_file:
            signed_xml_file.write(signed_xml_data)

    def verify_signed_xml(self, signed_xml_file_path):
        with open(signed_xml_file_path, "rb") as signed_xml_file:
            signed_xml_data = signed_xml_file.read()

        # Parse the XML data into an element
        signed_xml_element = etree.fromstring(signed_xml_data)

        cert = open(self.cert_path, "rb").read()
        verified = signxml.XMLVerifier().verify(signed_xml_element, x509_cert=cert)

        return verified

    def verify_owner(self, xml_file_path):
        with open(xml_file_path, "rb") as xml_file:
            xml_data = xml_file.read()

        # Parse the XML data into an element
        xml_element = etree.fromstring(xml_data)

        # Find the owner element
        owner_element = xml_element.find("owner")
        if owner_element is not None:
            return owner_element.text
        else:
            raise ValueError("Owner element not found in the XML file")

    def generate_hash(self, xml_file_path):
        with open(xml_file_path, "rb") as xml_file:
            xml_data = xml_file.read()

        hash_object = hashlib.sha256(xml_data)
        hash_value = hash_object.hexdigest()

        return hash_value

    def verify_hash(self, xml_file_path, hash_value):
        with open(xml_file_path, "rb") as xml_file:
            xml_data = xml_file.read()

        hash_object = hashlib.sha256(xml_data)
        computed_hash_value = hash_object.hexdigest()

        return computed_hash_value == hash_value

    def add_file_ownership(self, xml_file_path, owner, owned_by_file_path):
        with open(xml_file_path, "rb") as xml_file:
            xml_data = xml_file.read()

        # Parse the XML data into an element
        xml_element = etree.fromstring(xml_data)

        # Create an owner element
        owner_element = etree.Element("owner")
        owner_element.text = owner

        # Append the owner element to the XML element
        xml_element.append(owner_element)

        # Convert the XML element to a byte string
        updated_xml_data = etree.tostring(
            xml_element, encoding="UTF-8", xml_declaration=True
        )

        with open(owned_by_file_path, "wb") as owned_by_file:
            owned_by_file.write(updated_xml_data)

        return owned_by_file_path

    def change_file_ownership(self, xml_file_path, new_owner, owned_by_file_path):
        with open(xml_file_path, "rb") as xml_file:
            xml_data = xml_file.read()

        # Parse the XML data into an element
        xml_element = etree.fromstring(xml_data)

        # Find the owner element
        owner_element = xml_element.find("owner")
        if owner_element is not None:
            owner_element.text = new_owner
        else:
            raise ValueError("Owner element not found in the XML file")

        # Convert the XML element to a byte string
        updated_xml_data = etree.tostring(
            xml_element, encoding="UTF-8", xml_declaration=True
        )

        with open(owned_by_file_path, "wb") as owned_by_file:
            owned_by_file.write(updated_xml_data)

        # Return the path to the file with the new owner
        return owned_by_file_path

    def remove_file_ownership(self, xml_file_path):
        with open(xml_file_path, "rb") as xml_file:
            xml_data = xml_file.read()

        # Parse the XML data into an element
        xml_element = etree.fromstring(xml_data)

        # Find the owner element
        owner_element = xml_element.find("owner")
        if owner_element is not None:
            xml_element.remove(owner_element)
        else:
            raise ValueError("Owner element not found in the XML file")

        # Convert the XML element to a byte string
        updated_xml_data = etree.tostring(
            xml_element, encoding="UTF-8", xml_declaration=True
        )

        with open(xml_file_path, "wb") as updated_xml_file:
            updated_xml_file.write(updated_xml_data)

    def symmetric_encrypt(self, xml_file_path, encrypted_xml_file_path, key):
        with open(xml_file_path, "rb") as xml_file:
            xml_data = xml_file.read()

        f = Fernet(key)
        encrypted_data = f.encrypt(xml_data)

        with open(encrypted_xml_file_path, "wb") as encrypted_xml_file:
            encrypted_xml_file.write(encrypted_data)

    def symmetric_decrypt(self, encrypted_xml_file_path, decrypted_xml_file_path, key):
        with open(encrypted_xml_file_path, "rb") as encrypted_xml_file:
            encrypted_data = encrypted_xml_file.read()

        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)

        with open(decrypted_xml_file_path, "wb") as decrypted_xml_file:
            decrypted_xml_file.write(decrypted_data)

    def generate_key(self):
        return Fernet.generate_key()
