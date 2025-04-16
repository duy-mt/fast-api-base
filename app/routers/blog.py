from typing import List
from fastapi import APIRouter, Depends, status, HTTPException

# from ..authentication import oauth2

# from ..schemas.user import User
from ..schemas.blog import BlogCreate

from ..core import database
from sqlalchemy.orm import Session
from ..services.blog import BlogService

router = APIRouter(prefix="/blogs", tags=["Blogs"])

get_db = database.get_db


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: BlogCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(oauth2.get_current_user),
):
    # return BlogService.crex`ate_blog_service(request, db)
    return {'data': "hello"}

# @router.get("/", response_model=List[blog.show])
# def all(
#     db: Session = Depends(get_db),
#     # current_user: User = Depends(oauth2.get_current_user),
# ):
#     return blog.get_all(db)

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def destroy(
#     id: int,
#     db: Session = Depends(get_db),
#     # current_user: User = Depends(oauth2.get_current_user),
# ):
#     return blog.destroy(id, db)


# @router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
# def update(
#     id: int,
#     request: Blog,
#     db: Session = Depends(get_db),
#     # current_user: User = Depends(oauth2.get_current_user),
# ):
#     return blog.update(id, request, db)


# @router.get("/{id}", status_code=200, response_model=Blog.ShowBlog)
# def show(
#     id: int,
#     db: Session = Depends(get_db),
#     # current_user: User = Depends(oauth2.get_current_user),
# ):
#     return blog.show(id, db)
