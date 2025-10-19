# app/utils/security.py
from datetime import datetime, timedelta, timezone
import os
from jose import jwt
from pwdlib import PasswordHash

ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600  # 1 hour

# Read from environment or fallback to defaults
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH", "/app/keys/trino_private.pem")
PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH", "/app/keys/public_key.pem")
JWT_ISSUER = os.getenv("JWT_ISSUER", "http://localhost:7000")

# Initialize password hasher (Argon2 by default)
password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Hash a password for storing in the database."""
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    return password_hasher.verify(plain_password, hashed_password)

# Load private key (RS256 signing key)
with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()

def create_access_token(subject: str, extra_claims: dict = None) -> str:
    """
    Generate a JWT for the given subject (sub).
    Adds 'iss' field and optional extra claims.
    """
    payload = {
        "sub": subject,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS),
        "iss": JWT_ISSUER
    }

    if extra_claims:
        payload.update(extra_claims)

    token = jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)
    return token
