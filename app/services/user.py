from fastapi import HTTPException, status, Response, Cookie, Depends
from passlib.context import CryptContext
from ..schemas.user import SignUp, ShowUser, Login
from ..crud.user import create_user_by_email, get_user_by_email
from fastapi.responses import JSONResponse
from .auth import create_token, verify_token
from datetime import datetime, timedelta, timezone
from app.core.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user_logic(request: SignUp, db):
    # 1. Kiểm tra xem email đã tồn tại chưa
    existing_user = await get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # 2. Hash password
    hash_password = pwd_context.hash(request.password)

    # 3. Gọi crud insert db
    user_data = {
        "name": request.name,
        "email": request.email,
        "password": hash_password,
    }

    new_user = await create_user_by_email(db, user_data)

    # 4. return response

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User created successfully",
            "name": new_user["name"],
            "email": new_user["email"],
        },
    )


async def user_login_logic(request: Login, response: Response, db):
    # 1. Check email xem đã có trong db chưa
    existing_user = await get_user_by_email(db, request.email)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not registered"
        )

    # 2. Kiểm tra password
    is_password_correct = pwd_context.verify(
        request.password, existing_user["password"]
    )
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password or Email"
        )

    # 4. Tạo token
    token = create_token(
        existing_user["id"], existing_user["email"], expires_delta=timedelta(days=7)
    )

    # 3. Tạo Cookie
    response.delete_cookie("auth_token", domain="localhost", path="/")
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    response.set_cookie(
        key="auth_token",
        value=token,
        expires=expire,
        path="/",
        httponly=True,
        secure=False,
        samesite="lax",
    )
    return ShowUser(
        message="OK", name=existing_user["name"], email=existing_user["email"]
    )


async def verify_user(payload: dict = Depends(verify_token), db=Depends(get_db)):
    email = payload.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: no email"
        )

    return ShowUser(message="OK", name=payload["name"], email=payload["email"])


async def user_logout_logic(
    response: Response, db=Depends(get_db), payload: dict = Depends(verify_token)
):

    # 2. xóa cookie
    response.delete_cookie("auth_token", domain="localhost", path="/")

    # 3. return response
    return ShowUser(message="OK", name=payload["name"], email=payload["email"])
