import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_data(key: bytes, plaintext: bytes) -> tuple[bytes, bytes, bytes]:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    
    encrypted = aesgcm.encrypt(nonce, plaintext, None)
    
    ciphertext = encrypted[:-16]
    tag = encrypted[-16:]
    
    return nonce, ciphertext, tag
