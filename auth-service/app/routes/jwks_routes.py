# app/routes/jwks_routes.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import base64
from app.utils.security import PUBLIC_KEY_PATH

router = APIRouter(tags=["JWKS"])  # No prefix, so the URL matches exactly

# Load the public key once at startup
with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY_OBJ = serialization.load_pem_public_key(f.read())

def rsa_public_key_to_jwk(public_key: rsa.RSAPublicKey, kid: str = "trino-key-1") -> dict:
    """Convert RSA public key to a JWKS dict."""
    numbers = public_key.public_numbers()
    n = numbers.n
    e = numbers.e

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
    jwk = rsa_public_key_to_jwk(PUBLIC_KEY_OBJ)
    return JSONResponse(content={"keys": [jwk]})
