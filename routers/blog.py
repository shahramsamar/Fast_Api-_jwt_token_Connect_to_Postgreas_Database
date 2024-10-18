from fastapi import APIRouter, status, HTTPException, Query, Depends,Path
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.schema import NamesSchema, ResponseNamesSchema
from models.users import UserModel
from typing import Annotated, Optional, List
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import secrets
from fastapi.responses import JSONResponse
from auth.bearer import TokenBearer


router = APIRouter(tags=["Crud By Names"])
security = HTTPBasic()

@router.get("/names", response_model=List[ResponseNamesSchema],
            status_code=status.HTTP_200_OK)
async def names_list(user : bool = Depends(TokenBearer()),search: Optional[str] = Query(None, description="searching names"),
                     db: Session = Depends(get_db)):
    data = db.query(UserModel).all()
    return data

@router.post("/names",response_model=ResponseNamesSchema,status_code=status.HTTP_201_CREATED)
async def names_create(request:NamesSchema, user : bool = Depends(TokenBearer()),db:Session =Depends(get_db)):
    student_obj = UserModel(name=request.name,first_name=request.first_name,last_name=request.last_name)
    db.add(student_obj)
    db.commit()
    db.refresh(student_obj)
    return student_obj


@router.get("/names/{item_id}",response_model=ResponseNamesSchema,
            status_code=status.HTTP_200_OK)
async def names_detail(item_id: int = Path(description="something cool"),
                       user : bool = Depends(TokenBearer()), 
                       db:Session =Depends(get_db)):
    student_obj = db.query(UserModel).filter(UserModel.id == item_id).one_or_none()
    
    if not student_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="item not found")
    return student_obj



@router.put("/names/{item_id}",response_model=ResponseNamesSchema,
            status_code=status.HTTP_200_OK)
async def names_update(item_id: int, request:NamesSchema,
                        user : bool = Depends(TokenBearer()),
                        db:Session =Depends(get_db)):
    student_obj = db.query(UserModel).filter(UserModel.id == item_id).one_or_none()
    
    if not student_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="item not found")
    student_obj.name = request.name
    db.commit()
    db.refresh(student_obj)
    return student_obj


@router.delete("/names/{item_id}")
async def names_delete(item_id: int, user : bool = Depends(TokenBearer()),
                       db:Session =Depends(get_db)):
    student_obj = db.query(UserModel).filter(UserModel.id == item_id).one_or_none()
    
    if not student_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="item not found")
    db.delete(student_obj)
    db.commit()
    return JSONResponse({"detail": "item removed successfully"}, status_code=status.HTTP_200_OK)