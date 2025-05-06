from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, status, Depends
from ..crud.user import get_user_by_email
from app.core.database import get_db

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"


def create_token(user_id: str, email: str, expires_delta: timedelta):
    expire = datetime.utcnow() + expires_delta
    payload = {"sub": str(user_id), "email": email, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def verify_token(request: Request, db=Depends(get_db)):
    token = request.cookies.get("auth_token")
    if not token or token.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Not Received"
        )

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email = payload["email"]

        existing_user = await get_user_by_email(db, email)
        if not existing_user:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail="Token Not Received"
            )

        return existing_user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired"
        )
