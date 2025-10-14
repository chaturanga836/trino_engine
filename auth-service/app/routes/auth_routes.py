from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..models import database, user_model
from ..utils import security, jwt_handler

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing = db.query(user_model.User).filter(user_model.User.username == form_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = security.hash_password(form_data.password)
    new_user = user_model.User(username=form_data.username, password_hash=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt_handler.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/verify")
def verify(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint Trino calls to verify credentials."""
    user = db.query(user_model.User).filter(user_model.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"status": "success", "username": user.username}
