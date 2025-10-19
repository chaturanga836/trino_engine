# app/routes/jwks_routes.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import base64
from app.utils.security import PUBLIC_KEY_PATH

router = APIRouter(prefix="/jwks", tags=["JWKS"])

def pem_to_jwk(pem_path: str, kid: str = "trino-key-1") -> dict:
    """
    Convert RSA public key PEM file to JWKS format.
    """
    with open(pem_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise ValueError("Provided key is not an RSA public key")

    numbers = public_key.public_numbers()
    n = numbers.n
    e = numbers.e

    # Convert integers to base64url-encoded strings
    def int_to_base64url(x: int) -> str:
        b = x.to_bytes((x.bit_length() + 7) // 8, "big")
        return base64.urlsafe_b64encode(b).rstrip(b"=").decode("utf-8")

    jwk = {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "kid": kid,
        "n": int_to_base64url(n),
        "e": int_to_base64url(e),
    }
    return jwk

@router.get("/.well-known/jwks.json")
def jwks():
    jwk = pem_to_jwk(PUBLIC_KEY_PATH)
    return JSONResponse(content={"keys": [jwk]})
