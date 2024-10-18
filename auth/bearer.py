from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from models import TokenModel
from database.database import get_db
from datetime import datetime


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(TokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        credentials: HTTPAuthorizationCredentials = await super(TokenBearer, self).__call__(request)
        if credentials:
            # Corrected scheme check
            if credentials.scheme.lower() != "bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication schema.")
            
            # Verify the token and user
            user = self.verify_token(db, credentials.credentials)
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired token.")
            
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization code.")

    def verify_token(self, db, token: str):
        # Query the token from the database
        token_obj = db.query(TokenModel).filter(TokenModel.token == token).first()
        if token_obj:
            # Check if the token has expired
            if token_obj.expiration_date < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired.",
                )
            return token_obj.user

        return None
