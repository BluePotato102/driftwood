# aes_encryptor.py

import subprocess
import json

BINARY = "./encryptor"

def encrypt(data: dict):
    """Encrypt a Python dictionary and write to encrypted.json using C binary"""
    json_input = json.dumps(data, indent=2).encode()
    result = subprocess.run(
        [BINARY, "write"],
        input=json_input,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        raise RuntimeError("Encryption failed: " + result.stderr.decode())

def decrypt() -> dict:
    """Decrypt data from encrypted.json and return as a Python dictionary"""
    result = subprocess.run(
        [BINARY, "read"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        raise RuntimeError("Decryption failed: " + result.stderr.decode())

    return json.loads(result.stdout.decode())
