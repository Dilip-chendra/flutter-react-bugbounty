import pyotp
import hashlib
import secrets
from typing import Optional
from datetime import datetime, timedelta
import jwt
from cryptography.fernet import Fernet

class MFAAuthenticator:
    def __init__(self):
        self.secret_key = secrets.token_hex(32)
        self.fernet = Fernet(Fernet.generate_key())
        
    def generate_otp(self, user_id: str) -> str:
        """Generate a time-based OTP."""
        totp = pyotp.TOTP(self.secret_key)
        return totp.now()
    
    def verify_otp(self, user_id: str, otp: str) -> bool:
        """Verify the provided OTP."""
        totp = pyotp.TOTP(self.secret_key)
        return totp.verify(otp)
    
    def verify_biometric(self, biometric_data: bytes) -> bool:
        """Verify biometric data (implementation depends on hardware)."""
        try:
            # This is a placeholder. Actual implementation would use
            # platform-specific biometric APIs (e.g., TouchID, FaceID)
            return True
        except Exception as e:
            return False
    
    def authenticate_user(self, username: str, password: str, 
                         otp: Optional[str] = None,
                         biometric_data: Optional[bytes] = None) -> dict:
        """Complete authentication flow with MFA."""
        # First verify password (basic auth)
        if not self._verify_password(username, password):
            raise ValueError("Invalid username or password")
        
        # If OTP provided, verify it
        if otp and not self.verify_otp(username, otp):
            raise ValueError("Invalid OTP")
            
        # If biometric data provided, verify it
        if biometric_data and not self.verify_biometric(biometric_data):
            raise ValueError("Biometric verification failed")
            
        # Generate session token
        token = self._generate_session_token(username)
        
        return {
            "status": "success",
            "token": token,
            "requires_otp": not otp,
            "requires_biometric": not biometric_data
        }
    
    def _verify_password(self, username: str, password: str) -> bool:
        """Verify password using secure hashing."""
        # In production, fetch stored hash from database
        stored_hash = self._get_stored_password_hash(username)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode(), 
            b'salt', # In production, use unique salt per user
            100000  # Number of iterations
        )
        return secrets.compare_digest(password_hash, stored_hash)
    
    def _generate_session_token(self, username: str) -> str:
        """Generate a secure JWT session token."""
        payload = {
            'user': username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def _get_stored_password_hash(self, username: str) -> bytes:
        """Get stored password hash (placeholder)."""
        # In production, fetch from secure database
        return b'dummy_hash'  # Placeholder

# Usage example:
if __name__ == "__main__":
    auth = MFAAuthenticator()
    
    # Step 1: Initial login attempt
    try:
        result = auth.authenticate_user("user@example.com", "password123")
        if result["requires_otp"]:
            # Step 2: Get OTP from user
            otp = auth.generate_otp("user@example.com")
            # Verify with OTP
            result = auth.authenticate_user(
                "user@example.com", 
                "password123",
                otp=otp
            )
    except ValueError as e:
        print(f"Authentication failed: {e}") 