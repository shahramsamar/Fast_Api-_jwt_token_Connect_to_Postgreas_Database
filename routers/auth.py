from fastapi import APIRouter, status, HTTPException, Query, Path, Form, Body, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from sqlalchemy.orm import Session
from database.database import get_db, initiate_database
from models import AuthModel
from auth.utils import authenticate_user, generate_token
from schemas.schema import RegisterRequestSchema, RegisterResponseSchema
from auth.utils import get_password_hash

from schemas.schema import LoginResponseSchema, LoginRequestSchema



router = APIRouter(prefix="/api/v1", tags=["Authenticate"])

# Registration endpoint
@router.post("/register", response_model=RegisterResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(user: RegisterRequestSchema, db: Session = Depends(get_db)):
    # Check if the username already exists
    existing_user = db.query(AuthModel).filter(AuthModel.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create a new user
    new_user = AuthModel(
        username=user.username,
        password=hashed_password
    )

    # Save the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=LoginResponseSchema, status_code=status.HTTP_200_OK)
async def login(request: LoginRequestSchema, db: Session = Depends(get_db)):

    user = authenticate_user(
        db, username=request.username, password=request.password)
    token = generate_token(db, user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="username or password doesn't match")
    return {
        "detail": "successfully logged in",
        "token": token,
        "user_id": user.id
    }


