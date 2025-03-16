# Mitt Arv Security Fixes

This repository contains security fixes for the Mitt Arv application, addressing several critical vulnerabilities identified during the Beta Phase testing. Each fix is implemented as a standalone module that can be integrated into the main application.

## 🔒 Security Vulnerabilities Fixed

### 1. Multi-Factor Authentication (MFA)
**File**: `auth_mfa_fix.py`
- Implements OTP-based authentication
- Adds biometric login support
- Secures session token generation
- Uses PBKDF2 for password hashing

### 2. Session Management
**File**: `session_timeout_fix.py`
- Automatic session expiration after 15 minutes of inactivity
- Secure session token handling
- Background cleanup of expired sessions
- Middleware support for web frameworks

### 3. Data Encryption
**File**: `encrypt_storage_fix.py`
- AES-256 encryption for sensitive data
- Secure key derivation using PBKDF2
- PKCS7 padding implementation
- Support for both string and JSON data

### 4. Secure Data Wiping
**File**: `secure_uninstall_fix.py`
- Multi-pass data wiping (DoD-style)
- Secure directory traversal
- Verification of data removal
- Detailed logging of operations

### 5. Rate Limiting
**File**: `rate_limit_login_fix.py`
- Limits login attempts to 5 per minute
- IP-based blocking system
- Sliding window approach
- Automatic cleanup of old attempts

### 6. API Key Security
**File**: `secure_api_keys.py`
- Secure storage of API keys in environment variables
- Encryption of stored keys
- Key rotation support
- Metadata management

### 7. Trusted Contact Verification
**File**: `trusted_contact_verification.py`
- Multi-level verification (email, phone, biometric)
- Time-limited verification sessions
- Integration with email and SMS services
- Secure verification token handling

## 📋 Requirements

```bash
pip install -r requirements.txt
```

Required Python packages:
- cryptography>=41.0.0
- pyotp>=2.8.0
- python-dotenv>=1.0.0
- requests>=2.31.0
- twilio>=8.5.0
- jwt>=1.3.1
- PyJWT>=2.8.0

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/your-username/mitt-arv-security-fixes.git
cd mitt-arv-security-fixes
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 💡 Usage Examples

### Multi-Factor Authentication
```python
from auth_mfa_fix import MFAAuthenticator

auth = MFAAuthenticator()

# Step 1: Initial login
result = auth.authenticate_user("user@example.com", "password123")

# Step 2: Verify OTP
if result["requires_otp"]:
    otp = auth.generate_otp("user@example.com")
    result = auth.authenticate_user(
        "user@example.com", 
        "password123",
        otp=otp
    )
```

### Secure Data Storage
```python
from encrypt_storage_fix import SecureStorage

storage = SecureStorage("master-key")

# Encrypt sensitive data
sensitive_data = {
    "ssn": "123-45-6789",
    "credit_card": "4111-1111-1111-1111"
}

encrypted = storage.encrypt_data(sensitive_data)
decrypted = storage.decrypt_data(encrypted)
```

### Rate Limiting
```python
from rate_limit_login_fix import LoginManager

login_manager = LoginManager()

# Attempt login with rate limiting
result = login_manager.attempt_login(
    username="user@example.com",
    password="password123",
    ip_address="192.168.1.1"
)
```

## 🔧 Configuration

### Email Verification Settings
Update `contact_verification_config.json`:
```json
{
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your-email@gmail.com",
        "password": "your-app-specific-password"
    }
}
```

### SMS Verification Settings
Update Twilio credentials in `contact_verification_config.json`:
```json
{
    "sms": {
        "twilio_account_sid": "your-account-sid",
        "twilio_auth_token": "your-auth-token",
        "twilio_phone_number": "your-twilio-number"
    }
}
```

## 🛡️ Security Best Practices

1. **API Keys**: Never commit API keys or sensitive credentials to version control
2. **Environment Variables**: Use `.env` files for configuration
3. **Encryption Keys**: Rotate encryption keys periodically
4. **Logging**: Monitor and review security logs regularly
5. **Updates**: Keep all dependencies up to date

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔍 Security Auditing

Regular security audits are recommended to ensure:
- All security modules are properly configured
- Dependencies are up to date
- No new vulnerabilities have been introduced
- Logging and monitoring are functioning correctly

## ⚠️ Important Notes

1. This is a security-focused implementation. Review and adapt according to your specific needs.
2. Some implementations (like biometric verification) require platform-specific integration.
3. Always follow security best practices when deploying in production.
4. Regularly update dependencies to patch security vulnerabilities.
5. Monitor security logs and implement proper alerting mechanisms.

## 📞 Support

For security-related issues, please report them immediately to security@mittarv.com.
For general questions, create an issue in the repository. 