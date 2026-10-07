import unittest
from crypto.key_derivation import generate_salt, derive_key
from crypto.encryption import encrypt_data
from crypto.decryption import decrypt_data

class TestCrypto(unittest.TestCase):
    def test_encryption_decryption_success(self):
        password = "strongpassword123"
        salt = generate_salt()
        key = derive_key(password, salt, iterations=1000)
        
        plaintext = b"Ini adalah teks rahasia."
        nonce, ciphertext, tag = encrypt_data(key, plaintext)
        
        decrypted = decrypt_data(key, nonce, tag, ciphertext)
        self.assertEqual(decrypted, plaintext)

    def test_decryption_wrong_password(self):
        password = "strongpassword123"
        salt = generate_salt()
        key = derive_key(password, salt, iterations=1000)
        
        plaintext = b"Ini adalah teks rahasia."
        nonce, ciphertext, tag = encrypt_data(key, plaintext)
        
        wrong_key = derive_key("wrongpassword", salt, iterations=1000)
        
        with self.assertRaises(ValueError):
            decrypt_data(wrong_key, nonce, tag, ciphertext)

if __name__ == '__main__':
    unittest.main()
