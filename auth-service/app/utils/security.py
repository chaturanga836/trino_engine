# app/utils/security.py
from pwdlib import PasswordHash

# Create a recommended hasher (defaults to Argon2)
password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Hash a password for storing in the database."""
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    return password_hasher.verify(plain_password, hashed_password)
