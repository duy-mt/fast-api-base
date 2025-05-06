from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    message: str
    name: str
    email: EmailStr


class Login(BaseModel):
    email: EmailStr
    password: str


class SignUp(BaseModel):
    name: str
    email: EmailStr
    password: str
