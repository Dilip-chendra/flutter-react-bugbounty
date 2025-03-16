import pyotp
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, List
import json
import requests
from datetime import datetime, timedelta
import logging
import hashlib
import os

class TrustedContactVerifier:
    def __init__(self, config_file: str = "contact_verification_config.json"):
        """Initialize the trusted contact verifier."""
        self.config = self._load_config(config_file)
        self.logger = self._setup_logger()
        self.verification_cache: Dict[str, Dict] = {}
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for contact verification."""
        logger = logging.getLogger('TrustedContactVerifier')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from file."""
        if not os.path.exists(config_file):
            # Create default config
            default_config = {
                "email": {
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "sender_email": "your-email@gmail.com",
                    "password": "your-app-specific-password"
                },
                "sms": {
                    "twilio_account_sid": "your-account-sid",
                    "twilio_auth_token": "your-auth-token",
                    "twilio_phone_number": "your-twilio-number"
                },
                "verification_timeout_minutes": 10
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
        
        with open(config_file, 'r') as f:
            return json.load(f)
    
    def initiate_verification(self, contact_info: Dict) -> Dict:
        """Start the verification process for a trusted contact."""
        verification_id = self._generate_verification_id(contact_info)
        
        # Generate verification codes
        email_code = pyotp.random_base32()[:6]
        phone_code = pyotp.random_base32()[:6]
        
        # Store verification data
        self.verification_cache[verification_id] = {
            'contact_info': contact_info,
            'email_code': email_code,
            'phone_code': phone_code,
            'timestamp': datetime.utcnow(),
            'status': {
                'email': False,
                'phone': False,
                'biometric': False
            }
        }
        
        # Send verification codes
        self._send_email_verification(contact_info['email'], email_code)
        self._send_sms_verification(contact_info['phone'], phone_code)
        
        return {
            'verification_id': verification_id,
            'message': 'Verification codes sent to email and phone'
        }
    
    def verify_email_code(self, verification_id: str, code: str) -> bool:
        """Verify the email verification code."""
        if not self._is_verification_valid(verification_id):
            return False
            
        verification = self.verification_cache[verification_id]
        if verification['email_code'] == code:
            verification['status']['email'] = True
            return True
        return False
    
    def verify_phone_code(self, verification_id: str, code: str) -> bool:
        """Verify the phone verification code."""
        if not self._is_verification_valid(verification_id):
            return False
            
        verification = self.verification_cache[verification_id]
        if verification['phone_code'] == code:
            verification['status']['phone'] = True
            return True
        return False
    
    def verify_biometric(self, verification_id: str, biometric_data: bytes) -> bool:
        """Verify biometric data."""
        if not self._is_verification_valid(verification_id):
            return False
            
        # In production, implement actual biometric verification
        # This is a placeholder implementation
        verification = self.verification_cache[verification_id]
        verification['status']['biometric'] = True
        return True
    
    def is_fully_verified(self, verification_id: str) -> bool:
        """Check if all verification steps are completed."""
        if not self._is_verification_valid(verification_id):
            return False
            
        verification = self.verification_cache[verification_id]
        return all(verification['status'].values())
    
    def _generate_verification_id(self, contact_info: Dict) -> str:
        """Generate a unique verification ID."""
        data = f"{contact_info['email']}{contact_info['phone']}{datetime.utcnow()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _is_verification_valid(self, verification_id: str) -> bool:
        """Check if verification session is valid and not expired."""
        if verification_id not in self.verification_cache:
            return False
            
        verification = self.verification_cache[verification_id]
        timeout = timedelta(minutes=self.config['verification_timeout_minutes'])
        if datetime.utcnow() - verification['timestamp'] > timeout:
            del self.verification_cache[verification_id]
            return False
            
        return True
    
    def _send_email_verification(self, email: str, code: str) -> bool:
        """Send verification code via email."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['sender_email']
            msg['To'] = email
            msg['Subject'] = "Trusted Contact Verification"
            
            body = f"Your verification code is: {code}"
            msg.attach(MIMEText(body, 'plain'))
            
            context = ssl.create_default_context()
            with smtplib.SMTP(self.config['email']['smtp_server'], 
                            self.config['email']['smtp_port']) as server:
                server.starttls(context=context)
                server.login(self.config['email']['sender_email'],
                           self.config['email']['password'])
                server.send_message(msg)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}")
            return False
    
    def _send_sms_verification(self, phone: str, code: str) -> bool:
        """Send verification code via SMS using Twilio."""
        try:
            # Using Twilio API
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.config['sms']['twilio_account_sid']}/Messages.json"
            auth = (self.config['sms']['twilio_account_sid'], 
                   self.config['sms']['twilio_auth_token'])
            data = {
                "From": self.config['sms']['twilio_phone_number'],
                "To": phone,
                "Body": f"Your verification code is: {code}"
            }
            
            response = requests.post(url, auth=auth, data=data)
            return response.status_code == 201
            
        except Exception as e:
            self.logger.error(f"Error sending SMS: {str(e)}")
            return False

# Usage example:
if __name__ == "__main__":
    # Initialize verifier
    verifier = TrustedContactVerifier()
    
    # Example contact information
    contact = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
    }
    
    # Start verification process
    result = verifier.initiate_verification(contact)
    verification_id = result['verification_id']
    print("Verification initiated:", result)
    
    # Simulate verification steps
    email_verified = verifier.verify_email_code(verification_id, "123456")  # Use actual code
    print("Email verified:", email_verified)
    
    phone_verified = verifier.verify_phone_code(verification_id, "123456")  # Use actual code
    print("Phone verified:", phone_verified)
    
    biometric_verified = verifier.verify_biometric(verification_id, b"biometric_data")
    print("Biometric verified:", biometric_verified)
    
    # Check final verification status
    fully_verified = verifier.is_fully_verified(verification_id)
    print("Fully verified:", fully_verified) 