
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas import user
from fastapi import HTTPException,status
from utils.hashing import Hash

def create(request: user.User,db:Session):
    new_user = User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id:int,db:Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user