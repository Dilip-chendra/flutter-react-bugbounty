from datetime import datetime, timedelta
import jwt
from typing import Optional
import threading
import time

class SessionManager:
    def __init__(self, timeout_minutes: int = 15):
        self.timeout_minutes = timeout_minutes
        self.sessions = {}
        self.secret_key = "your-secret-key"  # In production, use secure key management
        self._start_cleanup_thread()
    
    def create_session(self, user_id: str) -> str:
        """Create a new session for a user."""
        session_token = self._generate_session_token(user_id)
        self.sessions[session_token] = {
            'user_id': user_id,
            'last_activity': datetime.utcnow(),
            'created_at': datetime.utcnow()
        }
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[str]:
        """Validate session and update last activity timestamp."""
        if session_token not in self.sessions:
            return None
            
        session = self.sessions[session_token]
        if self._is_session_expired(session):
            self.end_session(session_token)
            return None
            
        # Update last activity
        session['last_activity'] = datetime.utcnow()
        return session['user_id']
    
    def end_session(self, session_token: str) -> None:
        """End a user session."""
        if session_token in self.sessions:
            del self.sessions[session_token]
    
    def _generate_session_token(self, user_id: str) -> str:
        """Generate a secure session token using JWT."""
        payload = {
            'user_id': user_id,
            'created_at': datetime.utcnow().timestamp()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def _is_session_expired(self, session: dict) -> bool:
        """Check if session has expired due to inactivity."""
        last_activity = session['last_activity']
        return datetime.utcnow() - last_activity > timedelta(minutes=self.timeout_minutes)
    
    def _start_cleanup_thread(self) -> None:
        """Start background thread to clean up expired sessions."""
        def cleanup_worker():
            while True:
                expired_tokens = [
                    token for token, session in self.sessions.items()
                    if self._is_session_expired(session)
                ]
                for token in expired_tokens:
                    self.end_session(token)
                time.sleep(60)  # Check every minute
        
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()

# Example middleware for web frameworks
class SessionMiddleware:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
    
    def process_request(self, request):
        """Process incoming request and validate session."""
        session_token = request.headers.get('Authorization')
        if not session_token:
            return {'error': 'No session token provided'}, 401
            
        user_id = self.session_manager.validate_session(session_token)
        if not user_id:
            return {'error': 'Session expired'}, 401
            
        request.user_id = user_id
        return None

# Usage example:
if __name__ == "__main__":
    # Initialize session manager
    session_manager = SessionManager(timeout_minutes=15)
    
    # Create a new session
    user_id = "user123"
    session_token = session_manager.create_session(user_id)
    print(f"Created session: {session_token}")
    
    # Validate session
    validated_user = session_manager.validate_session(session_token)
    print(f"Validated user: {validated_user}")
    
    # Simulate inactivity
    time.sleep(2)
    
    # Validate again
    validated_user = session_manager.validate_session(session_token)
    print(f"Validated user after delay: {validated_user}")
    
    # End session
    session_manager.end_session(session_token)
    print("Session ended") 