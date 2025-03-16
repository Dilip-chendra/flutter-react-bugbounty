from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import threading
import time
import logging
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class LoginAttempt:
    timestamp: datetime
    success: bool
    ip_address: str

class RateLimiter:
    def __init__(self, max_attempts: int = 5, window_minutes: int = 1):
        """Initialize rate limiter with maximum attempts and time window."""
        self.max_attempts = max_attempts
        self.window_minutes = window_minutes
        self.attempts: Dict[str, List[LoginAttempt]] = defaultdict(list)
        self.blocked_ips: Dict[str, datetime] = {}
        self.lock = threading.Lock()
        self.logger = self._setup_logger()
        
        # Start cleanup thread
        self._start_cleanup_thread()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for rate limiter."""
        logger = logging.getLogger('RateLimiter')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def _start_cleanup_thread(self) -> None:
        """Start background thread to clean up old attempts."""
        def cleanup_worker():
            while True:
                self._cleanup_old_attempts()
                time.sleep(60)  # Run cleanup every minute
        
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()
    
    def _cleanup_old_attempts(self) -> None:
        """Remove attempts older than the window."""
        with self.lock:
            current_time = datetime.utcnow()
            window_start = current_time - timedelta(minutes=self.window_minutes)
            
            # Clean up attempts
            for ip in list(self.attempts.keys()):
                self.attempts[ip] = [
                    attempt for attempt in self.attempts[ip]
                    if attempt.timestamp > window_start
                ]
                if not self.attempts[ip]:
                    del self.attempts[ip]
            
            # Clean up blocked IPs
            for ip in list(self.blocked_ips.keys()):
                if self.blocked_ips[ip] <= current_time:
                    del self.blocked_ips[ip]
    
    def is_rate_limited(self, ip_address: str) -> Tuple[bool, int, datetime]:
        """Check if an IP is rate limited."""
        with self.lock:
            current_time = datetime.utcnow()
            
            # Check if IP is blocked
            if ip_address in self.blocked_ips:
                if self.blocked_ips[ip_address] > current_time:
                    remaining_time = self.blocked_ips[ip_address] - current_time
                    return True, 0, self.blocked_ips[ip_address]
                else:
                    del self.blocked_ips[ip_address]
            
            # Count recent attempts
            window_start = current_time - timedelta(minutes=self.window_minutes)
            recent_attempts = [
                attempt for attempt in self.attempts[ip_address]
                if attempt.timestamp > window_start
            ]
            
            remaining_attempts = self.max_attempts - len(recent_attempts)
            next_reset = window_start + timedelta(minutes=self.window_minutes)
            
            return len(recent_attempts) >= self.max_attempts, remaining_attempts, next_reset
    
    def record_attempt(self, ip_address: str, success: bool) -> None:
        """Record a login attempt."""
        with self.lock:
            current_time = datetime.utcnow()
            
            # Record the attempt
            self.attempts[ip_address].append(
                LoginAttempt(current_time, success, ip_address)
            )
            
            # If too many failed attempts, block the IP
            if not success:
                recent_failed = [
                    attempt for attempt in self.attempts[ip_address]
                    if not attempt.success and 
                    attempt.timestamp > current_time - timedelta(minutes=self.window_minutes)
                ]
                
                if len(recent_failed) >= self.max_attempts:
                    # Block for 15 minutes
                    block_until = current_time + timedelta(minutes=15)
                    self.blocked_ips[ip_address] = block_until
                    self.logger.warning(
                        f"IP {ip_address} blocked until {block_until} due to too many failed attempts"
                    )

class LoginManager:
    def __init__(self):
        """Initialize login manager with rate limiter."""
        self.rate_limiter = RateLimiter(max_attempts=5, window_minutes=1)
        self.logger = logging.getLogger('LoginManager')
    
    def attempt_login(self, username: str, password: str, ip_address: str) -> dict:
        """Handle a login attempt with rate limiting."""
        # Check rate limit
        is_limited, remaining_attempts, next_reset = self.rate_limiter.is_rate_limited(ip_address)
        
        if is_limited:
            return {
                'success': False,
                'message': f'Too many login attempts. Try again after {next_reset}',
                'remaining_attempts': 0
            }
        
        # Perform actual login (placeholder)
        success = self._verify_credentials(username, password)
        
        # Record the attempt
        self.rate_limiter.record_attempt(ip_address, success)
        
        if success:
            return {
                'success': True,
                'message': 'Login successful'
            }
        else:
            return {
                'success': False,
                'message': 'Invalid credentials',
                'remaining_attempts': remaining_attempts - 1
            }
    
    def _verify_credentials(self, username: str, password: str) -> bool:
        """Verify login credentials (placeholder)."""
        # In production, verify against secure database
        return username == "test" and password == "test123"

# Usage example:
if __name__ == "__main__":
    login_manager = LoginManager()
    
    # Simulate multiple login attempts
    test_ip = "192.168.1.1"
    
    # Successful login
    result = login_manager.attempt_login("test", "test123", test_ip)
    print("Login attempt 1:", result)
    
    # Failed login attempts
    for i in range(5):
        result = login_manager.attempt_login("test", "wrong_password", test_ip)
        print(f"Login attempt {i+2}:", result)
        
    # Try after being rate limited
    result = login_manager.attempt_login("test", "test123", test_ip)
    print("Login attempt after rate limit:", result) 