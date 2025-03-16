import os
from typing import Optional, Dict
import json
from pathlib import Path
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging
from dotenv import load_dotenv

class SecureKeyManager:
    def __init__(self, env_file: str = ".env", encrypted_store: str = ".secure_keys"):
        """Initialize secure key manager."""
        self.env_file = env_file
        self.encrypted_store = encrypted_store
        self.logger = self._setup_logger()
        
        # Load environment variables
        load_dotenv(self.env_file)
        
        # Initialize encryption
        self.encryption_key = self._get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the key manager."""
        logger = logging.getLogger('SecureKeyManager')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key from environment."""
        key = os.getenv('SECURE_KEY_ENCRYPTION_KEY')
        if not key:
            # Generate a new key
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(os.urandom(32)))
            
            # Store in environment
            with open(self.env_file, 'a') as f:
                f.write(f"\nSECURE_KEY_ENCRYPTION_KEY={key.decode()}")
            
            self.logger.info("Generated new encryption key")
            
        return key.encode() if isinstance(key, str) else key
    
    def store_api_key(self, key_name: str, api_key: str, metadata: Optional[Dict] = None) -> bool:
        """Securely store an API key."""
        try:
            # Prepare data for storage
            data = {
                'key': api_key,
                'metadata': metadata or {}
            }
            
            # Encrypt the data
            encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
            
            # Store in environment variable
            os.environ[self._env_key_name(key_name)] = encrypted_data.decode()
            
            # Update .env file
            self._update_env_file(key_name, encrypted_data.decode())
            
            self.logger.info(f"Successfully stored API key: {key_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing API key {key_name}: {str(e)}")
            return False
    
    def get_api_key(self, key_name: str) -> Optional[Dict]:
        """Retrieve a stored API key."""
        try:
            # Get from environment
            encrypted_data = os.getenv(self._env_key_name(key_name))
            if not encrypted_data:
                return None
            
            # Decrypt the data
            decrypted_data = self.fernet.decrypt(encrypted_data.encode())
            return json.loads(decrypted_data)
            
        except Exception as e:
            self.logger.error(f"Error retrieving API key {key_name}: {str(e)}")
            return None
    
    def delete_api_key(self, key_name: str) -> bool:
        """Delete a stored API key."""
        try:
            env_key = self._env_key_name(key_name)
            
            # Remove from environment
            if env_key in os.environ:
                del os.environ[env_key]
            
            # Update .env file
            self._remove_from_env_file(key_name)
            
            self.logger.info(f"Successfully deleted API key: {key_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting API key {key_name}: {str(e)}")
            return False
    
    def _env_key_name(self, key_name: str) -> str:
        """Generate standardized environment variable name."""
        return f"API_KEY_{key_name.upper()}"
    
    def _update_env_file(self, key_name: str, value: str) -> None:
        """Update or add a key in the .env file."""
        env_key = self._env_key_name(key_name)
        
        # Read existing content
        if os.path.exists(self.env_file):
            with open(self.env_file, 'r') as f:
                lines = f.readlines()
        else:
            lines = []
        
        # Find and replace or append
        key_found = False
        for i, line in enumerate(lines):
            if line.startswith(f"{env_key}="):
                lines[i] = f"{env_key}={value}\n"
                key_found = True
                break
        
        if not key_found:
            lines.append(f"{env_key}={value}\n")
        
        # Write back to file
        with open(self.env_file, 'w') as f:
            f.writelines(lines)
    
    def _remove_from_env_file(self, key_name: str) -> None:
        """Remove a key from the .env file."""
        env_key = self._env_key_name(key_name)
        
        if os.path.exists(self.env_file):
            with open(self.env_file, 'r') as f:
                lines = f.readlines()
            
            # Remove the key line
            lines = [line for line in lines if not line.startswith(f"{env_key}=")]
            
            with open(self.env_file, 'w') as f:
                f.writelines(lines)

# Usage example:
if __name__ == "__main__":
    # Initialize key manager
    key_manager = SecureKeyManager()
    
    # Store an API key
    key_manager.store_api_key(
        "EXAMPLE_SERVICE",
        "sk_test_123456789",
        metadata={
            "service": "Example API",
            "environment": "test"
        }
    )
    
    # Retrieve the API key
    stored_key = key_manager.get_api_key("EXAMPLE_SERVICE")
    if stored_key:
        print("Retrieved API key:", stored_key['key'])
        print("Metadata:", stored_key['metadata'])
    
    # Delete the API key
    key_manager.delete_api_key("EXAMPLE_SERVICE") 