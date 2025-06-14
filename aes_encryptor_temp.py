# aes_encryptor_temp.py

import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

KEY = b'01234567890123456789012345678901'  # 32 bytes
IV = b'0123456789012345'                   # 16 bytes
ENCRYPTED_FILE = "encrypted.json"

def _pad(data: bytes) -> bytes:
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()

def _unpad(padded_data: bytes) -> bytes:
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()

def encrypt(data: dict):
    """Encrypts the given dict and writes to ENCRYPTED_FILE"""
    plaintext = json.dumps(data, indent=2).encode()
    padded = _pad(plaintext)

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded) + encryptor.finalize()

    with open(ENCRYPTED_FILE, "wb") as f:
        f.write(encrypted)

def decrypt() -> dict:
    """Decrypts from ENCRYPTED_FILE and returns the original dictionary"""
    with open(ENCRYPTED_FILE, "rb") as f:
        encrypted = f.read()

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(encrypted) + decryptor.finalize()
    plaintext = _unpad(padded_plaintext)

    return json.loads(plaintext.decode())
