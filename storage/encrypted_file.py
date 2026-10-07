import struct
import base64

MAGIC_BYTES = b"AESWORD"
VERSION = 0x01
KDF_TYPE = 0x01

def pack_encrypted_data(iterations: int, salt: bytes, nonce: bytes, tag: bytes, ciphertext: bytes) -> str:
    """Pack metadata and ciphertext into a base64 string"""
    data = bytearray()
    data.extend(MAGIC_BYTES)
    data.extend(struct.pack('B', VERSION))
    data.extend(struct.pack('B', KDF_TYPE))
    data.extend(struct.pack('>I', iterations))
    data.extend(salt)
    data.extend(nonce)
    data.extend(tag)
    data.extend(ciphertext)
    return base64.b64encode(data).decode('utf-8')

def unpack_encrypted_data(b64_string: str) -> tuple[int, bytes, bytes, bytes, bytes]:
    """Unpack from base64 string"""
    try:
        data = base64.b64decode(b64_string)
    except Exception:
        raise ValueError("Format data tidak valid (bukan base64).")
        
    if len(data) < 7 + 1 + 1 + 4 + 16 + 12 + 16:
        raise ValueError("Data terlalu pendek. Data rusak atau bukan dari AES Word Encryptor.")
        
    magic = data[:7]
    if magic != MAGIC_BYTES:
        raise ValueError("File tidak valid atau bukan dari AES Word Encryptor")
    
    version = struct.unpack('B', data[7:8])[0]
    if version != VERSION:
        raise ValueError("Versi file tidak didukung")
        
    kdf_type = struct.unpack('B', data[8:9])[0]
    
    iterations = struct.unpack('>I', data[9:13])[0]
    salt = data[13:29]
    nonce = data[29:41]
    tag = data[41:57]
    ciphertext = data[57:]
    
    return iterations, salt, nonce, tag, ciphertext
