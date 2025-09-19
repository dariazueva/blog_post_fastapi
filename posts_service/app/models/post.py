from app.core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    category_id = Column(Integer)
