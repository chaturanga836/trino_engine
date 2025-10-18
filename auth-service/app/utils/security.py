# app/utils/security.py
from pwdlib.hash import bcrypt

def hash_password(password: str) -> str:
    """Hash a password for storing in the database."""
    return bcrypt.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    return bcrypt.verify(plain_password, hashed_password)
