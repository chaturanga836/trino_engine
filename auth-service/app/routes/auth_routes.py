from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import database, user_model
from app.schemas.user_schema import RegisterRequest, LoginRequest, VerifyRequest
from app.utils import security, jwt_handler

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(user_model.User).filter(user_model.User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = security.hash_password(payload.password)
    new_user = user_model.User(username=payload.username, password_hash=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.username == payload.username).first()
    if not user or not security.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt_handler.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/verify")
def verify(payload: VerifyRequest, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.username == payload.username).first()
    if not user or not security.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"status": "success", "username": user.username}
