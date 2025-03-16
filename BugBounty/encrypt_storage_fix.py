from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import os
from typing import Dict, Any, Union
import json

class SecureStorage:
    def __init__(self, master_key: str):
        """Initialize secure storage with a master key."""
        self.salt = os.urandom(16)
        self.key = self._derive_key(master_key.encode(), self.salt)
        self.fernet = Fernet(base64.urlsafe_b64encode(self.key))
    
    def _derive_key(self, master_key: bytes, salt: bytes) -> bytes:
        """Derive encryption key using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(master_key)
    
    def encrypt_data(self, data: Union[str, Dict[str, Any]]) -> str:
        """Encrypt data using AES-256."""
        if isinstance(data, dict):
            data = json.dumps(data)
        
        # Convert string to bytes if necessary
        if isinstance(data, str):
            data = data.encode()
            
        # Generate a unique IV for each encryption
        iv = os.urandom(16)
        
        # Create an AES cipher
        cipher = Cipher(
            algorithms.AES256(self.key),
            modes.CBC(iv)
        )
        
        # Pad the data
        padded_data = self._pad_data(data)
        
        # Encrypt the data
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Combine IV and encrypted data
        combined = iv + encrypted_data
        
        # Return base64 encoded string
        return base64.b64encode(combined).decode('utf-8')
    
    def decrypt_data(self, encrypted_data: str) -> Union[str, Dict[str, Any]]:
        """Decrypt data using AES-256."""
        # Decode from base64
        combined = base64.b64decode(encrypted_data.encode('utf-8'))
        
        # Extract IV and encrypted data
        iv = combined[:16]
        encrypted_data = combined[16:]
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES256(self.key),
            modes.CBC(iv)
        )
        
        # Decrypt
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Remove padding
        decrypted = self._unpad_data(decrypted_padded)
        
        # Try to parse as JSON
        try:
            return json.loads(decrypted)
        except json.JSONDecodeError:
            return decrypted.decode('utf-8')
    
    def _pad_data(self, data: bytes) -> bytes:
        """Add PKCS7 padding."""
        padding_length = 16 - (len(data) % 16)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    def _unpad_data(self, padded_data: bytes) -> bytes:
        """Remove PKCS7 padding."""
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]
    
    def secure_store(self, key: str, value: Any) -> None:
        """Securely store a key-value pair."""
        encrypted = self.encrypt_data(value)
        # In production, store in secure database
        print(f"Storing encrypted data for key {key}: {encrypted}")
        
    def secure_retrieve(self, key: str) -> Any:
        """Securely retrieve a stored value."""
        # In production, retrieve from secure database
        encrypted = "retrieved_encrypted_data"  # Placeholder
        return self.decrypt_data(encrypted)

# Usage example:
if __name__ == "__main__":
    # Initialize secure storage with a master key
    storage = SecureStorage("very-secure-master-key")
    
    # Example user data
    sensitive_data = {
        "ssn": "123-45-6789",
        "credit_card": "4111-1111-1111-1111",
        "address": "123 Secure St, Privacy Town, 12345"
    }
    
    # Encrypt and store
    encrypted = storage.encrypt_data(sensitive_data)
    print(f"Encrypted data: {encrypted}")
    
    # Decrypt and verify
    decrypted = storage.decrypt_data(encrypted)
    print(f"Decrypted data: {decrypted}")
    
    # Store in secure storage
    storage.secure_store("user_123", sensitive_data) 