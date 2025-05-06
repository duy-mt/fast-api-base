from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from app.core.database import get_db
from ..schemas import user
from ..services.user import (
    create_user_logic,
    user_login_logic,
    verify_user,
    user_logout_logic,
)
from ..services.auth import verify_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[user.ShowUser])
@router.post("/signup", response_model=user.ShowUser)
async def signup(request: user.SignUp, db=Depends(get_db)):
    return await create_user_logic(request, db)


@router.post("/login", response_model=user.ShowUser)
async def login(request: user.Login, response: Response, db=Depends(get_db)):
    return await user_login_logic(request, response, db)


@router.get("/auth-status", response_model=user.ShowUser)
async def auth_status(verify_user_response: dict = Depends(verify_user)):
    return verify_user_response


@router.get("/logout", response_model=user.ShowUser)
async def logout(logout_user_response: dict = Depends(user_logout_logic)):
    return logout_user_response
