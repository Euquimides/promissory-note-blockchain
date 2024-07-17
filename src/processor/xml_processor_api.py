from fastapi import FastAPI, UploadFile, File, Form, Query
from xml_processor import (
    XMLProcessor,
)  # Assuming xml_processor.py is in the same directory
import shutil

app = FastAPI()

xml_processor = XMLProcessor()


@app.post("/xml/sign")
async def sign_xml(
    xml_file: UploadFile = File(...), signed_xml_file_path: str = Form(...)
):
    with open(xml_file.filename, "wb") as buffer:
        shutil.copyfileobj(xml_file.file, buffer)
    xml_processor.sign_xml(xml_file.filename, signed_xml_file_path)
    return {
        "message": "XML signed successfully",
        "signed_xml_file_path": signed_xml_file_path,
    }


@app.post("/xml/verify-signed-xml")
async def verify_signed_xml(
    signed_xml_file_path: str = Query(
        ..., description="The path to the signed XML file"
    )
):
    # Implementation for verifying the signed XML
    # This is a placeholder for the actual verification logic
    verification_result = xml_processor.verify_signed_xml(signed_xml_file_path)
    return {"message": "Verification completed", "result": verification_result}


@app.post("/xml/verify-owner")
async def verify_owner(
    xml_file_path: str = Query(..., description="The path to the XML file")
):
    # Implementation for verifying the owner of the XML file
    # This is a placeholder for the actual verification logic
    owner = xml_processor.verify_owner(xml_file_path)
    return {"owner": owner}


@app.post("/xml/generate-hash")
async def generate_hash(xml_file: UploadFile = File(...)):
    with open(xml_file.filename, "wb") as buffer:
        shutil.copyfileobj(xml_file.file, buffer)
    hash_value = xml_processor.generate_hash(xml_file.filename)
    return {"hash": hash_value}


@app.post("/xml/add-ownership")
async def add_file_ownership(
    xml_file: UploadFile = File(...),
    owner: str = Form(...),
    owned_by_file_path: str = Form(...),
):
    with open(xml_file.filename, "wb") as buffer:
        shutil.copyfileobj(xml_file.file, buffer)
    owned_by_file_path = xml_processor.add_file_ownership(
        xml_file.filename, owner, owned_by_file_path
    )
    return {
        "message": "Owner added successfully",
        "owned_by_file_path": owned_by_file_path,
    }


@app.post("/xml/change-ownership")
async def change_file_ownership(
    xml_file: UploadFile = File(...),
    new_owner: str = Form(...),
    owned_by_file_path: str = Form(...),
):
    with open(xml_file.filename, "wb") as buffer:
        shutil.copyfileobj(xml_file.file, buffer)
    xml_processor.change_file_ownership(
        xml_file.filename, new_owner, owned_by_file_path
    )
    return {
        "message": "Owner changed successfully",
        "owned_by_file_path": owned_by_file_path,
    }


@app.post("/xml/remove-ownership")
async def remove_file_ownership(xml_file: UploadFile = File(...)):
    with open(xml_file.filename, "wb") as buffer:
        shutil.copyfileobj(xml_file.file, buffer)
    xml_processor.remove_file_ownership(xml_file.filename)
    return {"message": "Owner removed successfully"}


@app.post("/xml/encrypt")
async def symmetric_encrypt(
    xml_file: UploadFile = File(...),
    encrypted_xml_file_path: str = Form(...),
    key: str = Form(...),
):
    with open(xml_file.filename, "wb") as buffer:
        shutil.copyfileobj(xml_file.file, buffer)
    xml_processor.symmetric_encrypt(
        xml_file.filename, encrypted_xml_file_path, key.encode()
    )
    return {
        "message": "XML encrypted successfully",
        "encrypted_xml_file_path": encrypted_xml_file_path,
    }


@app.post("/xml/decrypt")
async def symmetric_decrypt(
    encrypted_xml_file_path: UploadFile = File(...),
    decrypted_xml_file_path: str = Form(...),
    key: str = Form(...),
):
    with open(encrypted_xml_file_path.filename, "wb") as buffer:
        shutil.copyfileobj(encrypted_xml_file_path.file, buffer)
    xml_processor.symmetric_decrypt(
        encrypted_xml_file_path.filename, decrypted_xml_file_path, key.encode()
    )
    return {
        "message": "XML decrypted successfully",
        "decrypted_xml_file_path": decrypted_xml_file_path,
    }


@app.post("/xml/generate-key")
async def generate_key():
    key = xml_processor.generate_key()
    return {"key": key.decode()}
