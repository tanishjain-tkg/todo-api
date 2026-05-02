from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.database import get_session
from app.models import User
from app.auth import hash_password, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Schema for register input
class RegisterInput(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: RegisterInput, session: Session = Depends(get_session)):
    # Check if user already exists
    existing = session.exec(select(User).where(User.email == data.email)).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    # Create new user
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User registered successfully", "email": user.email}

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    # Find user by email
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    # Create and return token
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}