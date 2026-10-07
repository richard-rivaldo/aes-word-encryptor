from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

def decrypt_data(key: bytes, nonce: bytes, tag: bytes, ciphertext: bytes) -> bytes:
    aesgcm = AESGCM(key)
    data_to_decrypt = ciphertext + tag
    try:
        plaintext = aesgcm.decrypt(nonce, data_to_decrypt, None)
        return plaintext
    except InvalidTag:
        raise ValueError("Dekripsi Gagal: Password salah atau data tidak valid")
