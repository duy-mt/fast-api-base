from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, Mapped

Base = declarative_base()

class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String)
    body: Mapped[str] = Column(String)
    published: Mapped[bool] = Column(Boolean, default=True)
