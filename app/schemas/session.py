from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from .chat import Chat


class Session(BaseModel):
    id: str
    userId: str
    title: Optional[str] = "New Chat"
    chats: List[Chat] = []
    createdAt: datetime


class ShowSession(BaseModel):
    id: str
    title: str


class CreateSession(BaseModel):
    email: EmailStr


class UpdateTitle(BaseModel):
    title: str
