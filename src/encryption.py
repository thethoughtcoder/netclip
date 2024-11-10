from cryptography.fernet import Fernet


class Encryption:
    def __init__(self, key=None):
        if key == b'generate_random_key_here':
            # Generate a new key and return it so it can be saved to config
            self.key = Fernet.generate_key()
        elif key:
            # Use provided key
            self.key = key
        else:
            # Fallback to generating new key
            self.key = Fernet.generate_key()
            
        try:
            self.cipher_suite = Fernet(self.key)
        except Exception as e:
            raise ValueError("Invalid encryption key. Must be valid base64-encoded Fernet key") from e

    def get_key(self) -> bytes:
        """Return the current key for saving to config"""
        return self.key

    def encrypt(self, data: bytes) -> bytes:
        return self.cipher_suite.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        return self.cipher_suite.decrypt(data) 