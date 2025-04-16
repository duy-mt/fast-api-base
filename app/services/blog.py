from ..schemas.blog import BlogCreate
from ..models.blog import Blog
from sqlalchemy.orm import Session
from ..crud.blog import create


class BlogService:

    @staticmethod
    def create_blog_service(request: BlogCreate, db: Session):
        # business logic, DB save giả định
        return create(request, db)
