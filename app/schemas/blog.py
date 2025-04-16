from pydantic import BaseModel
from typing import List


class BlogBase(BaseModel):
    title: str
    body: str
    published: bool


class BlogCreate(BlogBase):
    class Config:
        from_attributes = True


class Blog(BlogBase):
    class Config:
        from_attributes = True


class ShowBlog(BaseModel):
    title: str
    body: str

    class Config:
        from_attributes = True
