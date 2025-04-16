from sqlalchemy.orm import Session

from ..models.blog import Blog
from ..schemas.blog import BlogBase
from fastapi import HTTPException,status

def get_all(db: Session):
    blogs = db.query(Blog).all()
    return blogs

def create(request: Blog,db: Session):
    new_blog = Blog(title=request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int,db: Session):
    blog = db.query(Blog).filter(Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(id:int,request:Blog, db:Session):
    blog = db.query(Blog).filter(Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    blog.update(request)
    db.commit()
    return 'updated'

def show(id:int,db:Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
    return blog