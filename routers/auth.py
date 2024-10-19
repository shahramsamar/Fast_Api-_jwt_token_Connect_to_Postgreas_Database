from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from sqlalchemy.orm import Session
from database.database import get_db, settings
from models import StudentModel, UserModel
from schemas import *
from auth.utils import authenticate_user, generate_jwt_tokens, generate_access_token
import jwt
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["Authenticate with jwt"])

def create_user(request: LoginRequestSchema,
                db: Session = Depends(get_db)):
    user = UserModel(username=request.username, 
                     password=request.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/create-user-account",
             response_model=LoginResponseSchema,
             status_code=status.HTTP_201_CREATED)
def create_user_and_generate_tokens(request : LoginRequestSchema,
                                    db : Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, 
                            detail="Username already taken")
    
    # Create the user
    user = create_user(request, db)
    
    # Generate JWT tokens for the user
    jwt_tokens = generate_jwt_tokens(user)
    
    # Return user details and tokens
    return {
        "detail": "User account successfully created",
        "access_token": jwt_tokens["access_token"],
        "refresh_token": jwt_tokens["refresh_token"],
        "user_id": user.id
    }

@router.post("/login", 
             response_model=LoginResponseSchema, 
             status_code=status.HTTP_200_OK)
async def login(request : LoginRequestSchema,
                db : Session = Depends(get_db)):
    user = authenticate_user(db,
                             username=request.username,
                             password=request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="username or password doesn't match")

    jwt_tokens = generate_jwt_tokens(user)
    return {
        "detail": "successfully logged in",
        "access_token": jwt_tokens["access_token"],
        "refresh_token": jwt_tokens["refresh_token"],
        "user_id": user.id
    }


@router.post("/refresh",
             response_model=RefreshResponseSchema,
             status_code=status.HTTP_200_OK)
async def refresh_token(request: RefreshRequestSchema,
                        db: Session = Depends(get_db)):
    token = request.refresh_token
    try:
        result = jwt.decode(token, settings.SECRET_KEY, 
                            algorithms=["HS256"])
        expiration_time = datetime.fromtimestamp(result["exp"]).astimezone()

        if expiration_time < datetime.now().astimezone():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token or expired token. (exp)")
        if result["token_type"] != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token type.")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid or expired token. {e}")

    user_obj = db.query(UserModel).filter(UserModel.id == result["user_id"]).one_or_none()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User does not exist")

    payload = {
        "user_id": user_obj.id,
        "iat": datetime.now().astimezone()
    }

    return {"access_token": generate_access_token(payload)}
