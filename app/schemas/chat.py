from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class Chat(BaseModel):
    id: str
    role: str
    content: str
    createdAt: datetime


class ShowChat(BaseModel):
    role: str
    content: str
    createdAt: datetime


class ListChat(BaseModel):
    message: str
    chats: List[ShowChat]


class CreateChat(BaseModel):
    role: str
    content: str
    createdAt: datetime


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Message is required")
