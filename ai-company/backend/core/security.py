"""
Security & Authentication module for AI Company Command Center.
Includes SHA-256 password hashing, HMAC token issuance/verification, and rate limiting.
"""
import hmac
import hashlib
import base64
import time
import json
from typing import Optional, Dict, Any, Tuple

class SecurityManager:
    def __init__(self, secret_key: str = "ai-company-master-secret-key-2026"):
        self.secret_key = secret_key.encode('utf-8')
        self.rate_limit_records: Dict[str, list] = {} # ip/client -> [timestamps]

    def hash_password(self, password: str, salt: str = "ai_company_salt") -> str:
        return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

    def verify_password(self, password: str, password_hash: str, salt: str = "ai_company_salt") -> bool:
        computed = self.hash_password(password, salt)
        # Also check raw sha256 for backward compatibility with plain hash
        raw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hmac.compare_digest(computed, password_hash) or hmac.compare_digest(raw_hash, password_hash)

    def create_token(self, username: str, role: str = "owner", expires_in: int = 86400) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "sub": username,
            "role": role,
            "iat": int(time.time()),
            "exp": int(time.time() + expires_in)
        }
        b64_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
        b64_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        signature = hmac.new(self.secret_key, f"{b64_header}.{b64_payload}".encode(), hashlib.sha256).digest()
        b64_signature = base64.urlsafe_b64encode(signature).decode().rstrip("=")
        return f"{b64_header}.{b64_payload}.{b64_signature}"

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None
            b64_header, b64_payload, b64_signature = parts
            
            # Recompute signature
            expected_sig = hmac.new(self.secret_key, f"{b64_header}.{b64_payload}".encode(), hashlib.sha256).digest()
            sig_bytes = base64.urlsafe_b64decode(b64_signature + "=" * (-len(b64_signature) % 4))
            
            if not hmac.compare_digest(expected_sig, sig_bytes):
                return None
            
            payload_bytes = base64.urlsafe_b64decode(b64_payload + "=" * (-len(b64_payload) % 4))
            payload = json.loads(payload_bytes.decode())
            
            if payload.get("exp", 0) < time.time():
                return None
            
            return payload
        except Exception:
            return None

    def check_rate_limit(self, client_id: str, limit: int = 120, window_sec: int = 60) -> bool:
        now = time.time()
        if client_id not in self.rate_limit_records:
            self.rate_limit_records[client_id] = []
        # Filter timestamps
        self.rate_limit_records[client_id] = [t for t in self.rate_limit_records[client_id] if now - t < window_sec]
        if len(self.rate_limit_records[client_id]) >= limit:
            return False
        self.rate_limit_records[client_id].append(now)
        return True
