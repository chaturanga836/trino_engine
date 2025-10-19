from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import database, user_model
from app.schemas.user_schema import RegisterRequest, LoginRequest, VerifyRequest
from app.utils import security, jwt_handler

router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- Dependency for DB Session ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Register User ---
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(user_model.User).filter_by(username=payload.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    hashed = security.hash_password(payload.password)
    new_user = user_model.User(username=payload.username, password_hash=hashed)
    db.add(new_user)
    db.commit()

    return {"message": f"User '{payload.username}' registered successfully"}


# --- Login User (returns JWT token) ---
@router.post("/login", status_code=status.HTTP_200_OK)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter_by(username=payload.username).first()
    if not user or not security.verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Generate JWT Access Token
    token = jwt_handler.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


# --- Verify credentials ---
@router.post("/verify", status_code=status.HTTP_200_OK)
def verify(payload: VerifyRequest, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter_by(username=payload.username).first()
    if not user or not security.verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    return {"status": "success", "username": user.username}
