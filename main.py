from fastapi import FastAPI
from app.routers import blog
# from app.controllers.user import router as user
from app.core.database import engine


app = FastAPI()
# blog.Base.metadata.create_all(engine)
# user.Base.metadata.create_all(engine)
print("Router prefix:", blog.router.prefix) 
app.include_router(blog.router)    
# app.include_router(user)
